# free-gpt


Hello everyone using ChatGPT! I'm creating a free system for interacting with AI (just a hobby, it won't be as big and professional as SkyNet).
## Overview

This system works by using a cron job to initiate a chat session every minute, which asks the AI to perform a task. The AI responds with code snippets that are then executed automatically on a virtual machine, and the output is stored in a database. In the next cron job execution, the output from previous executions is added to the prompt.

So far, as part of an experiment, I have managed to instruct the AI to download a specific repository from a given user, and it successfully completed the task. If a required tool like Git was not installed, the AI installed it as well.

## Getting Started

To get started with this project, follow the instructions below:

1. Clone this repository to your local machine.
2. Set up a virtual environment and install the required dependencies.
3. Configure the necessary API keys and settings.
4. Run the main script to start interacting with the AI.

For more detailed instructions, please refer to the documentation provided within the repository.

## Contributing

If you'd like to contribute to this project, feel free to submit pull requests with your changes or improvements. We welcome any suggestions and ideas to make this system better and more versatile.
## License

This project is released under a free and open-source license. Please refer to the LICENSE file for more information.