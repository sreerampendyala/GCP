import argparse
import apache_beam as beam;

from .helpers.fhirDataConnector import FHIRDataConnector

from apache_beam.pipeline import PipelineOptions
from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json


class CarePlanTransform: 
    def __init__(self) -> None:
        with open('transformers/schemas/carePlan.json') as f:
            data = f.read()
            self.schemaString = '{"fields": ' + data + '}'
    
    def retriveData(self): 
        fhirDataConnector = FHIRDataConnector()
        return fhirDataConnector.search_resources_get('soy-alchemy-404117', 'northamerica-northeast1', 'medication_set', 'med_101', 'CarePlan')
    
    def transform(self):
        carePlanData = self.retriveData()
        self.schema = parse_table_schema_from_json(self.schemaString)

        fields = [f for f in self.schema.fields]

        rValue = []
        for record in carePlanData.get('entry'):
            row = {}

            for field in fields:
                row[field.name] = record.get('resource')[field.name]
            rValue.append(row)
        return rValue


    def run(self, argv=None) :
        parser = argparse.ArgumentParser();

        parser.add_argument('--output', dest='output', required=False, help='Output BQ table', default='medications.care_plan')

        known_args, pipeline_args = parser.parse_known_args(argv)

        p = beam.Pipeline(options=PipelineOptions(pipeline_args))

        data = self.transform()

        (p | 'Get rows' >> beam.Create(data)
           | 'Big Query write' >> beam.io.Write(
               beam.io.BigQuerySink(       
                known_args.output,
                schema=self.schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        ))

        p.run().wait_until_finish()


if __name__ == '__main__':
    CarePlanTransform().run()
