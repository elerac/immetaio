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
        t0_read = time.time()
        ret, frame = cap.read()
        t1_read = time.time()
        if not ret:
            print(f"Warning: Could not read frame {i}.")
            continue

        t0_write = time.time()
        immetaio.save(f"captured_images/frame{i}.png", frame, nonblock=nonblock)
        t1_write = time.time()

        t1 = time.time()
        fps = 1 / (t1 - t0)
        print(f"Frame {i:3d} at {fps:.2f} FPS (read: {(t1_read - t0_read) * 1000:.2f} ms, write: {(t1_write - t0_write) * 1000:.2f} ms)")
        t0 = t1

    print("Finished capturing frames.")

    # Explicitly wait for all non-blocking saves to complete.
    # This is NOT strictly necessary, if you don't access the saved files immediately after this point.
    immetaio.wait_saves()


if __name__ == "__main__":
    main()
