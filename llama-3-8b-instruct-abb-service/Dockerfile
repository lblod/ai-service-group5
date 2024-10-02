FROM ollama/ollama:latest

# Copy the Modelfile and GGUF file
COPY Modelfile /Modelfile
COPY llama-3-8b-instruct-abb.gguf /llama-3-8b-instruct-abb.gguf

# Expose the Ollama port
EXPOSE 11434

# Create a startup script
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'ollama create llama-3-8b-instruct-abb -f /Modelfile' >> /start.sh && \
    echo 'ollama serve' >> /start.sh && \
    chmod +x /start.sh

# Run the startup script
CMD ["/start.sh"]