# This is a special string that is used to signal to the LLM that it should retry the tool call.
# It works when the system prompt of the agent contains a reference to this string. The reason
# it is necessary to have a special string that signals the LLM should retry, is that we only
# want it to retry when EXPECTED errors occur (e.g. tool call surfaces a schema error), so that
# we can catch unexpected errors and debug them appropriately.
RETRY_SIGNAL = "[VALIDATION FAILED. RETRY.]"

# The failure prompt is used to guide the LLM to retry the tool call when it fails to validate the
# output. It gets appended after the error message, in retry prompts.
FAILURE_PROMPT = (
    "Wrong output. Consider the error and try again (use a tool call to validate)"
)

# The LLM model to use. TODO: make this configurable in the frontend.
LLM_MODEL = "openai:gpt-4o-mini"

# The system prompt is used to guide the LLM to generate a response that matches the given schema.
SYSTEM_PROMPT = """
You are a helpful assistant that generates a response that matches the given schema:
Your task is to generate a response that matches the given schema.

You must return a JSON object that is coherent with the following example:

{schema}

You must always use a tool call to validate your output.

⚠️ Important: The tool only accepts a single dictionary input argument. You must **wrap all fields into one object** and pass it as a single argument. Do not pass multiple top-level arguments.

If a tool call results in an error, one of the following scenarios will unfold:
1. You did not wrap your output in a single dictionary, and this results in a `ToolException` error. You fix your mistake and retry the tool call.
2. You did not return valid JSON or the JSON was not compliant with the specified schema, and an error ending with {RETRY_SIGNAL} is raised. You fix your mistake and retry the tool call.
3. Something else went wrong, and you receive an error message that does not fall into the above categories. You report the error to the developers.
"""
