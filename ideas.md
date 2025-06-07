# Hackathon Challenge Statements

## 19. Claims Analysis and fraud prediction in the insurance industry

### Challenge Statement
Fraudulent claims cost insurers over $7 billion annually, leading to increased premiums and financial losses.

### Domain
Insurance

### Recommended Technology Stack
Utilizing Fivetran for data integration and Fosfor for predictive analytics.

### Detailed Description
Detecting fraud efficiently is crucial to minimizing these costs, yet traditional methods face challenges such as data silos, manual processes, and outdated systems that hinder accurate and timely analysis.

The challenge is to develop a data-driven AI solution that can:
• Automate data integration from multiple sources into a centralized platform.
• Use AI-powered predictive analytics to detect fraudulent claims more accurately.
• Enhance data transformation and reporting for real-time insights.
• Reduce reliance on manual review and improve operational efficiency.
By leveraging AI and automation, insurers can streamline claims processing, improve fraud detection, and reduce financial losses, ultimately enhancing decision-making and customer satisfaction.


# approach
1. person -> previous claim and history
2. place and time
3. type of cliam
4. consistance 

# ai fine tuning
1. AI 
  a. system prompt - reseach more and get the ycombinator open prompt
  b. RAG - 
2. ai should explain it's decision
3. how many data points can we get out of these data



# data 
1. car accidents and resource claims 
2. police report - only if car is on movement 
  - no police report for parked cars 
  1. public insurance
  2. private insurance

- input
a. user description of the events
b. image of the accident (1 - 4 images)
c. users history - insurance history ( and accident history )
d. police report -  a pdf document
e. insurance 
e. cars history

# data processing 
1. resizing image for near - real time data processing and taking a standard format for the ai models
  a. 

# models choice 
a. google gemini 2.5 pro - multi modal 
d. gpt 4.1 - multi modal - azure openai 
b. LLABA from gemini
c. Bert / DeREberta for legal context

# Tools
1. cloud hosting - Azure
2. model hosting - not decided
3. frontend - a js framework that supports progressive loading, real-time update and server side rendering 
4. backend - python, backend service might be flask(not decided yet)
5. data ingestion pipeline: maybe azure databricks or synapse
6. data analysis
7. data store: object storage / adls gen2 for images, documents, highly optimized for real-time application db for metadata store, maybe cosmosdb ?
  a. adls gen2 with cosmosdb 
8. input validation: multi-staged check starting with file type checks to file content checks for pdf to virus scanning for user uploaded documents and pictures.    


https://studio.firebase.google.com/
Sylvia Suresh
12:22 AM
https://aistudio.google.com/apikey