import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_session_summary(log_file="logs/session_data.csv"):
    if not os.path.exists(log_file):
        print("No log file found. Run the system first!")
        return

    df = pd.read_csv(log_file, low_memory=False)
    
    # calculate stats
    avg_latency = df['Inference_Time_ms'].mean()
    total_alerts = df[df['Collision_Alert'] == 'YES'].shape[0]
    
    print("\n" + "="*30)
    print("   PERFORMANCE REPORT")
    print("="*30)
    print(f"Frames Analyzed:  {len(df)}")
    print(f"Avg Latency:      {avg_latency:.2f} ms")
    print(f"Target FPS:       {1000/avg_latency:.1f} FPS")
    print(f"Collision Events: {total_alerts}")
    print("="*30)

    # generate graph
    plt.figure(figsize=(10, 5))
    plt.plot(df['Inference_Time_ms'], label='Latency (ms)', color='blue')
    plt.axhline(y=avg_latency, color='r', linestyle='--', label='Average')
    plt.title('System Real-time Performance (CPU)')
    plt.xlabel('Frame Number')
    plt.ylabel('Milliseconds')
    plt.legend()
    plt.grid(True)
    
    # save graph as image
    graph_path = "logs/performance_graph.png"
    plt.savefig(graph_path)
    print(f"Graph saved to: {graph_path}")