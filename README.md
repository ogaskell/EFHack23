# EFHack23

## Files
- nextslide/
    - \_\_main\_\_.py

        Will create an app instance and run it. Should just be a stub

    - app.py

        Contains the main app class.
    - speech_reader.py

        Will use a generator to recieve mic input live and return timestamped text data.
    - doc_parser.py

        Contains classes for pasing documents (pptx, pdf, etc.)
    - prob_model.py

        Contains the actual predictors.
        - slide progress calcuator

            Will find the position within the current slide's bullet points.
            Uses RAKE-NLTK to extract keywords from both the speech and bullet points, and then meaning distance to pair speech with points.
            Should be able to switch between literal progress (i.e. point_n / total points) and point completion (i.e. number of points read), but implement point completion first.
        - transition calculator

            Calculate if we want to move the slide on.
            Needs to be conservative - we really don't want it to move if we don't want it to, but having to wait slightly longer or making someone ask to move it on isn't a big deal. Maybe listen for a keyword to move on too?

            Will essentially be position + pause length. I.e. if we're on the last point and pause for a few seconds, move on. But a few second pause mid slide doesn't me move on.
    - controllers.py

        Controls the presentation (passes keystrokes to the system or something similar)
