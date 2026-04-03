from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/jobs.db'
db = SQLAlchemy(app)

# Define a model class for the job
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')

def to_dict(job):
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "company": job.company,
        "status": job.status
    }

def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

@app.route('/jobs', methods=['POST'])
def add_job():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    allowed_fields = ['title', 'description', 'company', 'status']
    new_data = {key: value for key, value in data.items() if key in allowed_fields}

    required_fields = ['title', 'description']
    missing_fields = [field for field in required_fields if field not in new_data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    VALID_STATUS = ['pending', 'applied', 'rejected']
    if 'status' in new_data and new_data['status'] not in VALID_STATUS:
        return jsonify({'error': 'Invalid status'}), 400

    job = Job(**new_data)
    db.session.add(job)
    db.session.commit()
    logging.info("Job created")
    return jsonify(to_dict(job)), 201

@app.route('/jobs', methods=['GET'])
def get_jobs():
    status = request.args.get('status')
    title = request.args.get('title')

    query = Job.query
    if status:
        query = query.filter_by(status=status)
    if title:
        query = query.filter(Job.title.contains(title))

    jobs_list = query.all()
    return jsonify({'jobs': [to_dict(job) for job in jobs_list]})

@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    allowed_fields = ['title', 'description', 'company', 'status']
    new_data = {key: value for key, value in data.items() if key in allowed_fields}

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Not found'}), 404

    VALID_STATUS = ['pending', 'applied', 'rejected']
    if 'status' in new_data and new_data['status'] not in VALID_STATUS:
        return jsonify({'error': 'Invalid status'}), 400

    for key, value in new_data.items():
        setattr(job, key, value)

    db.session.commit()
    logging.info("Job updated")
    return jsonify(to_dict(job))

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Not found'}), 404

    db.session.delete(job)
    db.session.commit()
    logging.info("Job deleted")
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
