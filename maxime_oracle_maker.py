import os
import json

class OracleMaker(object):
    def __init__(self):
        self.topics_per_domain = None


    def get_topic_lists_per_domain(self, domain):
        ORIGINAL_DATA_PATH = f"originaldata/QMSUM/{domain}/jsonl"
        
        modes = ["train", "val", "test"]
        
        topics = []
        
        for mode in modes:
            with open(ORIGINAL_DATA_PATH + f"/{mode}.jsonl") as f:
                file_content = f.readlines()
                
            for item in file_content:
                json_item = json.loads(item)
                
                topics += [x["topic"] for x in json_item["topic_list"]]
                
        return set(topics)


    def get_topics_for_domains(self):
        self.topics_per_domain = {
            "Academic": self.get_topic_lists_per_domain("Academic"),
            "Committee": self.get_topic_lists_per_domain("Committee"),
            "Product": self.get_topic_lists_per_domain("Product"),
        }
        

    def generate_new_oracles(self):
        modes = ["train", "val", "test"]
        domains = ["Academic", "Committee", "Product"]
        
        for domain in domains:
            for mode in modes:
                ORACLES_PATH = f"data/QMSUM/qmsum_{mode}_with_oracle.jsonl"
                
                output_file = f"maximeOracles/{domain}/qmsum_{mode}_with_oracle.jsonl"

                # Reads the contents of the existing oracle file (qmsum_test_with_...)
                with open(ORACLES_PATH, "r") as oracle_file:
                    file_content = oracle_file.readlines()
                    
                # Iterate over the contents of the existing oracles. For each item, it 
                # gets the list of topics. If the topics are topics that are within the domain's topics,
                # then we write it to the output file.
                with open(output_file, "w") as out:
                    for item in file_content:
                        json_item = json.loads(item)
                        
                        topics = [x["topic"] for x in json_item["topic_list"]]
                        
                        if len(set(topics).intersection(self.topics_per_domain[domain])) > 0:
                            out.write(item)
                        

if __name__ == "__main__":
    oracle_maker = OracleMaker()
    oracle_maker.get_topics_for_domains()
    oracle_maker.generate_new_oracles()
    
    
    