# Team Project Architecture Plan

**Team Name:** Agent Ruche

**Project Name:** Agent Ruche

**Team Members:**

1. Vladislav Botnev 20230795
2. Cyrine Moalla 2023
3. Victoriya Mokhovikova 20230796
4. Khadija Belhamra 2023

**Project Domain:** Business  

---

## Part 1: Project Overview

### What problem are you solving?

Our startup focuses on helping call centres that handle a high volume of daily calls. We provide tools to analyse manager performance, track sales effectiveness and monitor the final outcomes of deals. By turning call data into insights, it will allow call centers to improve decision-making, boost productivity and increase overall sales success.

### Who will use your application?

Call Centers Team managers

### What's your core value proposition? (In one sentence)

To give feedback and insights from grand volume of daily calls

---

## Part 2: Define Your Layers

### UI Layer (Reflex)

**What pages/screens do you need?**

0. Login page: Login
   - Purpose: Allow user to register and login

1. Main page: Home Page
   - Purpose: Explain how the platform works and what are the tools

2. Additional page: File upload and goole drive integration (not sure about google drive) (Batch process calls)
   - Purpose: To let our clients provide the files to be transcribed and analyzed

3. Additional page: Chatbot page
   - Purpose: work with the context of phone call

**User Inputs:**

- ☐ File upload (PDF, images, CSV, etc.)
  - File types: .mp3, .wav
- ☐ Text input (questions, search, forms)
  - For: Gather addititonal insights from calls
- ☐ Dropdown selections
  - Options:
    - Transcribe dialogue
    - Text analysis
    - Overall assessment and conclusion
    - Agreements from the conversation
    - Rating on a 10-point scale
    - Rating details

**What do you display to users?**

- Extracted structured data
- Chat conversation
- Metrics/statistics

---

### Service Layer (Business Logic)

**What services does your domain need?**

Think about major features/capabilities.

**Service 1:** Upload Service

Purpose: load the file for future analysis

Main responsibilities

- Get the file
- Check the format
- Check restrictions (file size)

**Service 2:** Transcribe Service

Purpose: perform speech to text conversion

Main responsibilities

- Download the file from upload service
- Run the trancription (Whisper) model
- Respond with text output

**Service 3:** Analysis Service

Purpose: Receive the plain text (transcription) of the phone call and to perform the analysis

Main responsibilities

- Receive the text from transcribe service
- Use LLM to extract knowlegde from text

---

### AI Layer (Gemini Operations)

**What AI operations do you need?**

Check all that apply and describe:

- ☐ **Chat/Q&A with context**
  - About what: phone calls transcriptions

- ☐ **Summarization**
  - Summarize what: phone calls transcriptions

- ☐ **Text generation**
  - Generate what: analysis and extract agreements

- ☐ **Analysis**
  - Analyze what: phone calls transcriptions

**Will you need multi-turn conversations?**

☐ Yes

If yes, for what purpose: to make the user experience more seemless

---

## Part 3: Data Flow

**Map your primary workflow:**

Choose your most important user action and trace it through the system.

**User Action:** upload phone call record and choose the desired actions

(e.g., "User uploads medical record and asks 'What medications am I taking?'")

**Step-by-Step Flow:**

```
1. User does: upload documents
        ↓
2. Streamlit (app.py) calls: upload service
        ↓
3. Which service: upload service
   What does it do:
   a. saves the file on server and make a db record
   b. calls for transcription service
        ↓
4. Which service: transcription service
   What does it do:
   a. receives the file
   b. use whisper to extract text from file
   c. save the transcript to db 
   d. calls for analysis service
        ↓
4. AI Service called for: analysis service
   Input:  recieves the transcript
   Output: extracted analysis and agreemts
        ↓
6. Data returned to UI: json with fields with transcription, agreements, analysis, score
        ↓
7. User sees: parsed json
```

**Draw a diagram on paper/whiteboard showing this flow!**

---

## Part 4: Data Schema

### What structured data do you extract?

**Your Domain Schema:**

```json
{
  "transcription": "string and plain text of transcription of the file",
  "agreements": "string and plain text of agreements extracted from the file",
  "score": "number and numerical representation of how good the phone call went",
  "analysis": "string and analysis of transcription on what can be done better and how the call went overall"
}
```

**Required fields (must have):**

- transcription
- agreements
- score
- analysis

---

## Part 5: Team Roles

**Who builds what:**

**Member 1:** Vladislav Botnev → Responsible for: backend integrations (db and flow)

**Member 2:** ⁠Khadija Belhamra → Responsible for: frontend

**Member 3:** Cyrine Moalla → Responsible for: AI service inside (backend for analysis)

**Member 4:** Vika Mokhovikova → Responsible for: AI service outside (conversation)

---

## Part 6: Next Steps

**This week:**

- Set up project structure
- Create main service
- Test AI operations

**Next 2 weeks:**

- Build Streamlit UI
- Connect services
- Add tracing with Langfuse

**Final weeks:**

- Polish and improve UX
- Test thoroughly
- Deploy to Streamlit Cloud
- Prepare presentation

---
