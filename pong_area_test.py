#fichier de test

#actu : test les colisions


from fps_limiter import LimitFPS, FPSCounter

fps_limiter = LimitFPS(fps=30)
fps_counter = FPSCounter()

while True:
    if fps_limiter():
    
        print("current fps: %s" % fps_counter())