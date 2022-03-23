from flask import Flask, request, jsonify, make_response
from InvoiceParser import InvoiceParser
from flask_cors import CORS

app = Flask(__name__)

# Document AI's Access Data.
app.config['GCLOUD'] = {
   'project_id': '164490247589',
   'location': 'us',
   'processor_id': '8c8383f6ce3fc315'
}

CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
   pdfFile = request.files['PDF_FILE']
   invoiceParser = InvoiceParser(**app.config['GCLOUD'])

   feedback = invoiceParser.parse(pdfFile)

   response = make_response(jsonify({
      'data': feedback
   }))

   response.status_code = 200

   return response


if __name__ == '__main__':
    app.run(debug=True)
