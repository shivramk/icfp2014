(define (at map ghostlocs x y)
  (set! row (getlistelem map y))
  (if (contains? ghostlocs (cons x y) cmploc) 6
      (getlistelem row x)))

(define (contains? list elem cmp)
  (if (atom? list) 0
    (if (cmp elem (car list)) 1
      (contains? (cdr list) elem cmp))))

(define (cmploc l1 l2)
  (and (= (car l1) (car l2)) (= (cdr l1) (cdr l2))))

(define (max a b)
  (if (> a b) a b))

(define (max4 a b c d)
  (max a (max b (max c d))))

(define (maxidx1 list curidx maxidx maxval)
  (if (atom? list) maxidx
    (if (> (car list) maxval)
      (maxidx1 (cdr list) (+ curidx 1) curidx (car list))
      (maxidx1 (cdr list) (+ curidx 1) maxidx maxval))))

(define (maxidx l)
  (maxidx1 (cdr l) 1 0 (car l)))

(define (item-score v)
  (if (= v 0) -1000000
    (if (= v 1) 1
      (if (= v 2) 10
        (if (= v 3) 50
          (if (= v 4) 100
            (if (= v 5) 1 (do (debug -7777) -2000000))))))))

(define (score width height map ghostlocs x y s depth)
  (if (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) 0
    (if (<= depth 0) s
      (if (< s -100000) s
          (best-score width height map ghostlocs x y s (- depth 1)
                      (item-score (at map ghostlocs x y)))))))

(define (best-score width height map ghostlocs x y s depth v)
   (max4
     (score width height map ghostlocs (- x 1) y (+ s v) depth)
     (score width height map ghostlocs (+ x 1) y (+ s v) depth)
     (score width height map ghostlocs x (- y 1) (+ s v) depth)
     (score width height map ghostlocs x (+ y 1) (+ s v) depth)))

(define (penalty s d oppd)
  (if (= d oppd)
    (- s 30) s))

(define (mod x y)
  (- x (* (/ x y) y)))

(define (map list func)
  (if (atom? list) list
    (cons (func (car list)) (map (cdr list) func))))

(define (getloc x) (getlistelem x 1))

(define (make_move worldstate)
  (set! worldmap (gettupleelem worldstate 0))
  (set! lambdastate (gettupleelem worldstate 1))
  (set! height (len worldmap))
  (set! width (len (getlistelem worldmap 0)))
  (set! lpos (gettupleelem lambdastate 1))
  (set! x (gettupleelem lpos 0))
  (set! y (gettupleelem lpos 1))
  (set! dir (gettupleelem lambdastate 2))
  (set! ghoststate (gettupleelem worldstate 2))
  (set! ghostlocs (map ghoststate getloc))
  (set! oppdir (mod (+ 2 dir) 4))
  (set! sleft  (penalty (score width height worldmap ghostlocs (- x 1) y 0 4) 3 oppdir))
  (set! sright (penalty (score width height worldmap ghostlocs (+ x 1) y 0 4) 1 oppdir))
  (set! sup    (penalty (score width height worldmap ghostlocs x (- y 1) 0 4) 0 oppdir))
  (set! sdown  (penalty (score width height worldmap ghostlocs x (+ y 1) 0 4) 2 oppdir))
  (debug lpos)
  (debug ghostlocs)
  (debug sup)
  (debug sright)
  (debug sdown)
  (debug sleft)
  (maxidx (cons sup (cons sright (cons sdown (cons sleft 0))))))

(define (step aistate worldstate) 
  (cons 0 (make_move worldstate)))

(define (main worldstate undocumented) 
  (cons 0 step))
