import argparse
import torch
import scipy
import numpy as np

from transformers import PreTrainedTokenizer, T5ForConditionalGeneration, T5Tokenizer, AdamW, set_seed


class Oneforall:
    def __init__(self, model_name_or_path, tokenizer_name_or_path, device):
        self.model = T5ForConditionalGeneration.from_pretrained(model_name_or_path, torch_dtype=torch.float16)
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name_or_path)
        self.device = device
        self.model.to(device)

    def predict(self, question: str, context: str, min_length: int) -> str:
        self.model.eval()
        inputs = self.tokenizer.encode(f"question: {question}  context: {context}", return_tensors="pt")
        inputs = inputs.to(self.device)
        outputs = self.model.generate(inputs, min_length=min_length, max_length=256, num_return_sequences=30, num_beams=210, early_stopping=True, num_beam_groups=30, diversity_penalty=0.5)
        outputs = self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        # return top 5 percent of the outputs sort by count
        output_counts = {output: outputs.count(output) for output in outputs}
        output_counts = {k: v for k, v in sorted(output_counts.items(), key=lambda item: item[1], reverse=True)}
        # compute ranks of the outputs based on their counts if count is the same the rank is the same
        out = list(np.array(list(output_counts.keys()))[scipy.stats.rankdata(list(np.array(list(output_counts.values()))*-1), method="min") <= 5])

        return out












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
        ['strongly associates with occupation',1], # occupation
        ['has strong persona',1], # persona
        ["strongly relates with personality type",1], # personality
        ["has strong ncskills",1], # ncskills
        ["strongly motivates to", 1], # motivation to
        ["strongly motivates for", 1], # motivation for
        ["strongly relates to skill",1], # skill
        ["as a result, person makes others feel",1], # feel
        ["relates to concepts",1], # concepts
        ["is for job",1], # job
        ["has strong traits",1], # traits
        ["is for field of study",1], # field of study
        ["relates to fieldOfStudy",1], # field of study
        ["relates to task",3], # task
    ]


    print(f"Question: {question}")
    for context in contexts:    
        print(f"Context: {context}")
        print(f"Answer: {oneforall.predict(question, context[0], min_length=context[1])}")
        print("")

    print("Done")