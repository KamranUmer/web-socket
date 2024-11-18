import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:6789"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the chat server")

            async def send_message():
                while True:
                    try:
                        message = await asyncio.to_thread(input, "You: ")
                        await websocket.send(message)
                    except Exception as e:
                        print(f"Error sending message: {e}")
                        break
            
            async def receive_message():
                while True:
                    try:
                        response = await websocket.recv()
                        print(f"Server: {response}")
                    except websockets.ConnectionClosed:
                        print("Server connection closed.")
                        break

            # Run send and receive loops concurrently
            await asyncio.gather(send_message(), receive_message())
    except Exception as e:
        print(f"Connection error: {e}")

# Run the client
asyncio.run(chat_client())
