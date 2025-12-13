import cv2
import sys

# Helper function to create trackers compatible with different OpenCV versions
def create_tracker_by_name(tracker_type):
    # OpenCV 4.5+ moves many trackers to 'legacy'
    if tracker_type == 'MOSSE':
        try:
            return cv2.legacy.TrackerMOSSE_create()
        except AttributeError:
            return cv2.TrackerMOSSE_create() # Older OpenCV versions
            
    elif tracker_type == 'KCF':
        try:
            return cv2.legacy.TrackerKCF_create()
        except AttributeError:
            return cv2.TrackerKCF_create()
            
    elif tracker_type == 'CSRT':
        try:
            return cv2.TrackerCSRT_create() # CSRT is usually in the main module
        except AttributeError:
            return cv2.legacy.TrackerCSRT_create()
            
    else:
        print(f"Invalid tracker: {tracker_type}")
        return None

# ==========================================
# 1. MOSSE Tracker (The Speed King)
# ==========================================
def run_mosse_tracker():
    print("[INFO] Starting MOSSE Tracker (Fastest)...")
    tracker = create_tracker_by_name('MOSSE')
    run_tracking_loop(tracker, "MOSSE")

# ==========================================
# 2. KCF Tracker (The Middle Ground)
# ==========================================
def run_kcf_tracker():
    print("[INFO] Starting KCF Tracker (Balanced)...")
    tracker = create_tracker_by_name('KCF')
    run_tracking_loop(tracker, "KCF")

# ==========================================
# 3. CSRT Tracker (The Accuracy King)
# ==========================================
def run_csrt_tracker():
    print("[INFO] Starting CSRT Tracker (Most Accurate)...")
    tracker = create_tracker_by_name('CSRT')
    run_tracking_loop(tracker, "CSRT")

# ==========================================
# Standard Tracking Loop (Shared Logic)
# ==========================================
def run_tracking_loop(tracker, name):
    # 1. Open Webcam
    video = cv2.VideoCapture(0)
    
    # 2. Read the first frame
    ok, frame = video.read()
    if not ok:
        print("Error: Could not read video")
        return

    # 3. Select ROI (Draw the box manually)
    print(">>> DRAW a box around the object and press ENTER <<<")
    bbox = cv2.selectROI("Tracking", frame, False)
    
    # 4. Initialize tracker with the first frame and box
    tracker.init(frame, bbox)

    while True:
        ok, frame = video.read()
        if not ok: break

        # 5. Update tracker (Where did it go?)
        timer = cv2.getTickCount()
        success, box = tracker.update(frame)
        
        # Calculate FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # 6. Draw the result
        if success:
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1) # Green Box
            cv2.putText(frame, f"{name} detected", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking Failure", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Show FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        cv2.imshow("Tracking", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# ==========================================
# Main Menu
# ==========================================
if __name__ == "__main__":
    print("-------------------------------")
    print("SELECT TRACKER:")
    print("1. CSRT  (Best for general use)")
    print("2. MOSSE (Best for speed/old CPUs)")
    print("3. KCF   (Good balance)")
    print("-------------------------------")
    
    choice = input("Enter number (1-3): ")

    if choice == '1':
        run_csrt_tracker()
    elif choice == '2':
        run_mosse_tracker()
    elif choice == '3':
        run_kcf_tracker()
    else:
        print("Invalid choice. Exiting.")