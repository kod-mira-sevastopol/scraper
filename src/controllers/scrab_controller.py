from flask import jsonify, Blueprint, request
import src.services.scraber_service as scraber_service

scrab_controller = Blueprint('scrab_controller', __name__)

@scrab_controller.route('/resume/scrab', methods=['POST'])
async def get_scrab():
    if 'file' not in request.files and 'url' not in request.form:
        return jsonify({'error': 'No file or URL part'}), 400

    if 'file' in request.files:
        return await process_file(request.files['file'])
    elif 'url' in request.form:
        return process_url(request.form['url'])

    return jsonify({'error': 'Invalid request'}), 400


async def process_file(resume_file):
    if resume_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if resume_file:
        result = await scraber_service.Scraber.scrab_file(resume_file)

        if result is None:
            return jsonify({'error': 'Result is none'}), 400

        return jsonify(result)

    return jsonify({'error': 'Invalid file'}), 400


def process_url(resume_url):
    if resume_url == '':
        return jsonify({'error': 'No URL provided'}), 400

    if 'hh.ru' in resume_url:
        result = scraber_service.Scraber.scrab_url(resume_url)
        if result is None:
            return jsonify({'error': 'Invalid URL or unable to fetch'}), 400
        return jsonify(result)
    else:
        return jsonify({'error': 'Invalid URL'}), 400

@scrab_controller.route('/resume/preview')
def get_preview():
    result = scraber_service.Scraber.scrabed_preview()
    return jsonify(result)
