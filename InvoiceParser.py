class InvoiceParser:
    def __init__(self, project_id: str, location: str, processor_id: str):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id


    def get_text(self, doc_element: dict, document: dict):
        response = ''

        for segment in [doc_element.text_anchor.text_segments[0]]:
            start_index = (
                int(segment.start_index)
                if segment in doc_element.text_anchor.text_segments
                else 0
            )
            end_index = int(segment.end_index)
            response += document.text[start_index:end_index]

        return response

    def parse(self, pdfile):

        from google.cloud import documentai_v1 as documentai

        options = {}

        if self.location == 'eu':
            options = {'api_endpoint': 'https://eu-documentai.googleapis.com'}

        client = documentai.DocumentProcessorServiceClient(
            client_options=options)

        name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"  # noqa: E501

        # read file content
        content = pdfile.read()

        # Prepare document
        document = {"content": content, "mime_type": "application/pdf"}

        # Prepare a new request.
        request = {"name": name, "raw_document": document}

        # make the request
        result = client.process_document(request)

        # Read the obtained-document pages
        document = result.document
        pages = document.pages

        response = dict()

        for page in pages:
            for form_field in page.form_fields:
                field_name = self.get_text(form_field.field_name, document)
                field_value = self.get_text(form_field.field_value, document)
                response[field_name.strip().lower()] = field_value.strip()

        return response

