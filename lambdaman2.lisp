(define (at map x y)
  (set! row (getlistelem map y))
  (getlistelem row x))

(define (analyzepos map x y val)
  (if (!= (at map x y) 0)
    (if (!= (at map x y) 6) val -1) -1))

(define (analyzepos2 map x y val)
  (if (= (at map x y) 2) val
    (if (= (at map x y) 3) val
      (if (= (at map x y) 4) val -1))))

(define (make_move worldstate)
  (set! worldmap (gettupleelem worldstate 0))
  (set! lambdastate (gettupleelem worldstate 1))
  (set! height (len worldmap))
  (set! width (len (getlistelem worldmap 0)))
  (set! lpos (gettupleelem lambdastate 1))
  (set! x (gettupleelem lpos 0))
  (set! y (gettupleelem lpos 1))
  (set! legal 0)
  (set! l1 (if (> y 0) (analyzepos worldmap x (- y 1) 0) -1))
  (set! l2 (if (< x (- width 1)) (analyzepos worldmap (+ x 1) y 1) -1))
  (set! l3 (if (< y (- height 1)) (analyzepos worldmap x (+ y 1) 2) -1))
  (set! l4 (if (> x 0) (analyzepos worldmap (- x 1) y 3) -1))
  (set! m1 (if (> y 0) (analyzepos2 worldmap x (- y 1) 0) -1))
  (set! m2 (if (< x (- width 1)) (analyzepos2 worldmap (+ x 1) y 1) -1))
  (set! m3 (if (< y (- height 1)) (analyzepos2 worldmap x (+ y 1) 2) -1))
  (set! m4 (if (> x 0) (analyzepos2 worldmap (- x 1) y 3) -1))
  (debug (at worldmap x y))
  (if (!= m4 -1) m4
    (if (!= m2 -1) m2
      (if (!= m1 -1) m1
        (if (!= m3 -1) m3
          (if (!= l1 -1) l1
            (if (!= l4 -1) l4
              (if (!= l3 -1) l3
                (if (!= l2 -1) l2 0)))))))))

(define (step aistate worldstate) 
  (cons 0 (make_move worldstate)))

(define (main worldstate undocumented) 
  (cons 0 step))
