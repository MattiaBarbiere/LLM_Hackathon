# LLM_Hackation
LLM Hackathon @ EPFL 2025

## Todo

### Handlers
- [ ] message handler
  - [ ] routing messages depending on state
  - [ ] accepting routes if currently processing a state (state true or false, for long delays)
- [ ] input handler
  - [ ] adding input to game state
  - [ ] state change only if enough inputs we have
  - [ ] processing images for object detection and appending to inputs list
- [ ] qa handler
  - [ ] Question and answer queries
  - [ ] Only transition to end state if the answer is acceptable
  - [ ] generating hints, images, answers and everything.

### Game State
- [ ] Inputs, storing maybe some images?
- [ ] State transition function

### Telegram bot logic (main.py)
- [ ] Implement basic image, and other modalities
- [ ] Get main state instance
