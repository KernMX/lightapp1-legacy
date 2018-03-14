# Visualization Setup vvv
## Courtesy of
 https://github.com/scottlawsonbc/audio-reactive-led-strip

## My Change
- microphone.py
  - Changed infinite loop in start_stream(callback)
  - while True --> while running
  - running is a global variable
