import asyncio
import websockets

# Set to store connected clients
connected_clients = set()

async def handle_client(websocket):
    # Add new client to the set
    connected_clients.add(websocket)
    print(f"New client connected from ")
    
    try:
        async for message in websocket:
            print(f"Message received: {message}")
            # Broadcast message to all connected clients
            disconnected_clients = []
            for client in connected_clients:
                try:
                    if client != websocket:
                        await client.send(message)
                except websockets.ConnectionClosed:
                    # Track disconnected clients
                    disconnected_clients.append(client)
            # Remove any disconnected clients
            for client in disconnected_clients:
                connected_clients.remove(client)
    except websockets.ConnectionClosed as e:
        print(f"Client disconnected. Reason: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Ensure client is removed from the set
        connected_clients.remove(websocket)
        print("Cleaned up disconnected client.")

async def start_server():
    print("Server started on ws://localhost:6789")
    async with websockets.serve(handle_client, "localhost", 6789):
        await asyncio.Future()  # Run forever

# Start the server
asyncio.run(start_server())
