from typing import List, Dict, Optional, Any
from langchain_core.messages import AIMessage, BaseMessage

def extract_final_response(result: Dict[str, Any], final_answer_tool_name: str) -> Optional[str]:
    """
    Extracts the final answer from a LangGraph result state.

    Checks for a specific tool call in the last AIMessage first,
    then falls back to the content of the last AIMessage.

    Args:
        result: The dictionary result from graph.invoke().
                Expected to have a "messages" key.
        final_answer_tool_name: The exact name of the tool used to submit
                                 the final answer (e.g., "SubmitFinalAnswer").

    Returns:
        The extracted answer string, or None if no suitable answer is found.
    """
    print("--- Processing Final Result ---")
    final_state_messages: List[BaseMessage] = result.get("messages", [])

    if not final_state_messages:
        print("Error: No messages found in the final state.")
        return None

    final_msg = final_state_messages[-1]
    print(f"Final message type: {type(final_msg).__name__}")

    extracted_answer = None
    is_tool_call_answer = False
    found_specific_tool = False

    # 1. Check for the specific tool call in the last AIMessage
    if isinstance(final_msg, AIMessage) and final_msg.tool_calls:
        print(f"Found {len(final_msg.tool_calls)} tool call(s) in the final message.")
        for tool_call in final_msg.tool_calls:
            # Check if THIS tool call is the one we want
            if tool_call.get("name") == final_answer_tool_name:
                found_specific_tool = True
                is_tool_call_answer = True # Mark that answer came from the correct tool
                print(f"  Processing '{final_answer_tool_name}' tool call.")
                args = tool_call.get("args")
                if isinstance(args, dict):
                    # Assumes the answer is in the 'answer' key of the args dict
                    extracted_answer = args.get("answer")
                    if extracted_answer is None:
                        print(f"  Tool '{final_answer_tool_name}' called, but 'answer' argument missing/None.")
                        print(f"  Tool call arguments: {args}")
                else:
                    print(f"  Tool '{final_answer_tool_name}' called, but 'args' not a dictionary.")
                    print(f"  Tool call arguments: {args}")
                # Once found and processed, break the loop
                break
            else:
                print(f"  Ignoring tool call: {tool_call.get('name')}") # Log other calls found

        if not found_specific_tool:
             print(f"Found tool calls, but none were '{final_answer_tool_name}'.")

    # 2. Fallback: Check direct AI content ONLY if the specific tool wasn't found/processed
    if not found_specific_tool and isinstance(final_msg, AIMessage) and final_msg.content:
        print(f"No '{final_answer_tool_name}' tool call processed. Checking direct AI content.")
        extracted_answer = final_msg.content
        is_tool_call_answer = False # Mark that it came from content

    # 3. Final Logging
    if extracted_answer:
        source = "Tool Call" if is_tool_call_answer else "AI Content"
        print(f"Successfully extracted answer from: {source}")
    else:
        print("Could not extract a final answer via tool call or direct content.")
        print("Final Message Details:")
        print(final_msg) # Print the whole message for debugging if no answer found

    print("--- Finished Processing Result ---")
    return extracted_answer