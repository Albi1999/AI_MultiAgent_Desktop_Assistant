# AI Desktop Assistant
This project demonstrates how to build an AI desktop assistant that can interact with a computer's desktop environment using Claude's vision capabilities. It includes a Streamlit interface for interacting with the assistant and a VNC server for displaying the desktop.

> [!IMPORTANT]
> This repository is inspired bt the [Anthropic Demo Repository](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo).

## Quickstart
To quickly run the demo, you can use Docker. Make sure you have Docker installed on your machine.
### Prerequisites
- Docker installed
- An API key for Anthropic
- (Optional) AWS credentials for Bedrock or Google Cloud credentials for Vertex AI
## Running the demo

### Anthropic API

> [!TIP]
> You can find your API key in the [Anthropic Console](https://console.anthropic.com/).

```bash
docker run \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -it computer-use-demo:ai-desktop-assistant
```

Once the container is running, see the [Accessing the demo app](#accessing-the-demo-app) section below for instructions on how to connect to the interface.

### Accessing the demo app

Once the container is running, open your browser to [http://localhost:8080](http://localhost:8080) to access the combined interface that includes both the agent chat and desktop view.

The container stores settings like the API key and custom system prompt in `~/.anthropic/`. Mount this directory to persist these settings between container runs.

Alternative access points:

- Streamlit interface only: [http://localhost:8501](http://localhost:8501)
- Desktop view only: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)
- Direct VNC connection: `vnc://localhost:5900` (for VNC clients)

## Screen size

Environment variables `WIDTH` and `HEIGHT` can be used to set the screen size. For example:

```bash
docker run \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -e WIDTH=1920 \
    -e HEIGHT=1080 \
    -it computer-use-demo:ai-desktop-assistant
```

We do not recommend sending screenshots in resolutions above [XGA/WXGA](https://en.wikipedia.org/wiki/Display_resolution_standards#XGA) to avoid issues related to [image resizing](https://docs.anthropic.com/en/docs/build-with-claude/vision#evaluate-image-size).
Relying on the image resizing behavior in the API will result in lower model accuracy and slower performance than implementing scaling in your tools directly. The `computer` tool implementation in this project demonstrates how to scale both images and coordinates from higher resolutions to the suggested resolutions.

When implementing computer use yourself, we recommend using XGA resolution (1024x768):

- For higher resolutions: Scale the image down to XGA and let the model interact with this scaled version, then map the coordinates back to the original resolution proportionally.
- For lower resolutions or smaller devices (e.g. mobile devices): Add black padding around the display area until it reaches 1024x768.
