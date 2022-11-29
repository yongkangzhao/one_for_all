import argparse


from transformers import PreTrainedTokenizer, T5ForConditionalGeneration, T5Tokenizer, AdamW, set_seed


class Oneforall:
    def __init__(self, model_name_or_path, tokenizer_name_or_path, device):
        self.model = T5ForConditionalGeneration.from_pretrained(model_name_or_path)
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name_or_path)
        self.device = device
        self.model.to(device)

    def predict(self, question: str, context: str) -> str:
        self.model.eval()
        inputs = self.tokenizer.encode(f"question: {question}  context: {context}", return_tensors="pt")
        inputs = inputs.to(self.device)
        outputs = self.model.generate(inputs, max_length=256, num_return_sequences=5, num_beams=25, early_stopping=True)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)












if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--device', default='cuda', type=str,
                        help='device to be used for computations (in {cpu, cuda:0, cuda:1, ...}, default: cpu)')

    parser.add_argument('--max_input_length', type=int, default=512,
                        help='Maximum lenght of input text, (default: 512, maximum admitted: 512)')

    parser.add_argument('--seed', type=int, default=7,
                        help='Seed for random initialization (default: 7)')

    parser.add_argument('--load-check-point-model', type=str, default=None,
                        help='Load a check point to continue training')

    parser.add_argument('--load-check-point-tokenizer', type=str, default=None,
                        help='Load a check point to continue training')                    

    args = parser.parse_args()

    oneforall = Oneforall(args.load_check_point_model, args.load_check_point_tokenizer, args.device)

    question = """
    M&A/investment and strategy executive with diverse industry experience in Corporate M&A (Cisco, NetApp, Expedia Group), Management Consulting (McKinsey, BCG), and Financial Services (Morgan Stanley).

    Unique background in corporate development & strategy, strategic planning, financial modeling and valuation, and enterprise consulting.

    Led 13 international acquisitions ranging from sub-$10M to $870M in value, totaling at about $2B.
    Led 6 investments and served as Board Observer of 3 SaaS/Subscription-based companies.

    Led Cisco's Corporate Long-range Strategic Planning and Operations Reviews for 2 years covering over $35B of revenue and underlying budget planning.
    
    Functional Specialties:
    Corporate Development (Mergers and Acquisition, Investment, Strategic Partnership / Joint Venture, Divestiture), Corporate and New Business Strategy, Go-to-Market Strategy, Strategic Planning, Corporate Finance, Private Equity

    Industry/Technology Specialties:
    Software, SaaS / PaaS, Artificial Intelligence / Machine Learning, Cloud Computing & Orchestration, Kubernetes, IT Infrastructure Management, Big Data Analytics, Internet of Things / Edge Computing, Data Security, Storage / Converged / HyperConverged Infrastructure, Data Virtualization, Cloud Services Brokerage, Networking, Telecom, Financial Services / Fintech
    """

    contexts = [
        "concept_is_related_to_fieldOfStudy",
        "concept_is_related_to_job",
        "fieldOfStudy_is_good_for_occupation",
        "fieldOfStudy_is_related_to_skill",
        "fieldOfStudy_needs_concept,",
        "fieldOfStudy_requires_concept",
        "job_is_related_to_occupation",
        "job_motivated_to",
        "job_need_to_do_skill",
        "job_need_understand_skill",
        "job_perceived_as_perception",
        "ncskills_are_helpful_for_task",
        "occupation_associates_with_personality",
        "occupation_has_fieldOfStudy",
        "occupation_is_perceived_as_perception",
        "occupation_is_related_to_task",
        "occupation_motivated_by",
        "occupation_need_traits",
        "occupation_needs_concept",
        "persona_has_ncskills",
        "persona_has_traits",
        "persona_is_perceived_as_perception",
        "persona_motivated_by",
        "personality_associates_with_occupation",
        "personality_is_related_to_motivation",
        "personality_is_seen_as_perception",
        "skill_is_related_to_job",
        "skill_is_related_to_skill",
        "tasks_associates_with_feel",
        "tasks_associates_with_occupation",
        "tasks_makes_others_feel",
        "tasks_needs_skill",
        "tasks_requires_skill",
    ]
    print(f"Question: {question}")
    for context in contexts:    
        print(f"Context: {context}")
        print(f"Answer: {oneforall.predict(question, context)}")
        print("")
        

    print("Done")