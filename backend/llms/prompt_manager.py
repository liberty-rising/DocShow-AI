class PromptManager:
    def __init__(self):
        pass

    def create_chart_config_prompt(
        self, msg: str, table_metadata: str, chart_type: str, nivo_config_preview: dict
    ):
        prompt = f"""
            Generate a responsive chart configuration based on the following request.
            Focus on optimizing the configuration for responsiveness, ensuring the chart is clearly visible and legible on a variety of screen sizes.

            User request:
            {msg}
            Metadata about the table:
            {table_metadata}
            Chart type:
            Responsive {chart_type}
            Current nivo configuration:
            {nivo_config_preview}

            Provide output in JSON format as follows:
            {{
                "title":"",
                "query":"",
                "nivoConfig":{{}}
            }}

            The 'nivoConfig' should be complete or updated based on the user's requests.
            The 'data' key in 'nivoConfig' shows a preview of the data; do not update it.
            The 'keys' key in 'nivoConfig' should be updated based on the names of the query columns.
            The 'indexBy' key in 'nivoConfig' should be set to the name of the column which should be used to index the data.
            Prioritize responsive design to ensure the chart adapts well to different screen sizes.
            Do not set the parameters 'width' and 'height' as the charts are all 'Responsive' versions of themselves.
        """
        return prompt

    def create_get_table_name_from_sample_prompt(
        self, sample_content: str, extra_desc: str, table_metadata: str
    ):
        prompt = f"""
            Based on the sample data and existing table metadata, determine to which table the sample data should be appended.

            Sample Data:
            {sample_content}

            Existing Table Metadata:
            {table_metadata}

            Return only the name of the table.
            """
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: {extra_desc}"
        return prompt

    def create_table_create_prompt(
        self,
        sample_content: str,
        header: str,
        existing_table_names: str,
        extra_desc: str,
    ):
        prompt = "Generate SQL CREATE TABLE statement for the following sample data:"
        if header:
            prompt += f"\n\nHeader:\n{header}"
        prompt += f"\n\nSample data:\n{sample_content}"
        if existing_table_names:
            prompt += f"\n\nDo not use the following table names as they are already in use: \n{existing_table_names}"
        if extra_desc:
            prompt += (
                f"\n\nAdditional information about the sample data: \n{extra_desc}"
            )
        return prompt

    def create_table_desc_prompt(
        self,
        create_query: str,
        sample_content: str,
        extra_desc: str,
    ):
        prompt = f"""
            Generate a brief description for the table that will be created using the SQL CREATE TABLE query below.
            This description should help in determining whether to categorize new data into this table
            and should also provide the context needed to generate suggested queries for reports and analytics in the future.

            SQL CREATE TABLE Query:
            {create_query}

            Sample Data:
            {sample_content}

            Only generate the description, no formatting or title. Do not include any additional text, explanations, or filler words.
            """
        if extra_desc:
            prompt += f"\n\nAdditional information about the sample data: {extra_desc}"
        return prompt

    def jpg_data_extraction_prompt(self, instructions: str):
        prompt = f"""
            Extract the following data from the given JPG file:

            User request:
            {instructions}

            Provide output in a JSON string using the requested information as keys.
            The JSON string should be flat, not nested.

            Example output:
            {{
                {{
                    "client_name":"John Doe",
                    "invoice_amount":"1000",
                    "date":"01-01-2021"
                }},
                {{
                    "client_name":"Jane Doe",
                    "invoice_amount":"2000",
                    "date":"01-01-2021"
                }}
            }}
            In this example, the requested information would have been client name, invoice amount, and date.

            Return only the requested information, no additional text or formatting.
            """
        return prompt
