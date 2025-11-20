#!/usr/bin/env python3
import argparse
from backend.monitor import monitor

def main():
    parser = argparse.ArgumentParser(
        description="Port Intent Detector PRO: CLI real-time monitor"
    )
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="Polling interval in seconds (default 2.0)"
    )

    args = parser.parse_args()
    print(f"Starting Port Intent Detector PRO CLI with interval={args.interval}s")
    monitor(poll_interval=args.interval)

if __name__ == "__main__":
    main()
