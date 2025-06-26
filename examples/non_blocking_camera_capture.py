import time
import cv2
import immetaio


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    nonblock = True
    print(f"Using non-blocking mode: {nonblock}")

    t0 = time.time()
    for i in range(60):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {i}.")
            continue

        immetaio.save(f"captured_images/frame{i}.png", frame, nonblock=nonblock)

        t1 = time.time()
        fps = 1 / (t1 - t0)
        print(f"Frame {i:3d} at {fps:.2f} FPS")
        t0 = t1

    print("Finished capturing frames.")

    # Explicitly wait for all non-blocking saves to complete.
    # This is NOT strictly necessary, if you don't access the saved files immediately after this point.
    immetaio.wait_saves()


if __name__ == "__main__":
    main()
