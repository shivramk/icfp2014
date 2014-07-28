(define (at map ghostlocs fruit x y)
  (set! row (getlistelem map y))
  (set! ghosts (contains? ghostlocs (cons 0 (cons x y)) cmploc2))
  (if (atom? ghosts)
    (do 
      (set! val (getlistelem row x))
      (if (= val 4)
        (if (> fruit 0) val 0) val))
    (if (= (car ghosts) 1) 7 6)))

(define (contains? list elem cmp)
  (if (atom? list) 0
    (if (cmp elem (car list)) (car list)
      (contains? (cdr list) elem cmp))))

(define (cmploc l1 l2)
  (and (= (car l1) (car l2)) (= (cdr l1) (cdr l2))))

(define (cmploc2 l1 l2)
  (and (= (cadr l1) (cadr l2)) (= (cddr l1) (cddr l2))))

(define (min a b)
  (if (< a b) a b))

(define (max a b)
  (if (> a b) a b))

(define (min4 a b c d)
  (min a (min b (min c d))))

(define (max4 a b c d)
  (max a (max b (max c d))))

(define (maxidx1 list curidx maxidx maxval)
  (if (atom? list) maxidx
    (if (> (car list) maxval)
      (maxidx1 (cdr list) (+ curidx 1) curidx (car list))
      (maxidx1 (cdr list) (+ curidx 1) maxidx maxval))))

(define (minidx1 list curidx minidx minval)
  (if (atom? list) minidx
    (if (< (car list) minval)
      (minidx1 (cdr list) (+ curidx 1) curidx (car list))
      (minidx1 (cdr list) (+ curidx 1) minidx minval))))

(define (find1 list elem cmp)
  (if (atom? list) 0
    (if (cmp (car list) elem) 1
      (find1 (cdr list) elem cmp))))

(define (maxidx l)
  (maxidx1 (cdr l) 1 0 (car l)))

(define (minidx l)
  (minidx1 (cdr l) 1 0 (car l)))

(define (item-score v)
  (cond ((= v 0) -1000000)
        ((= v 1) 1)
        ((= v 2) 10)
        ((= v 3) 50)
        ((= v 4) 100)
        ((= v 5) 1)
        (else -1000)))

(define (score width height map ghostlocs x y s depth)
  (cond ((or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) s)
        ((<= depth 0) s)
        ((< s -100000) s)
        (else (best-score width height map ghostlocs x y s (- depth 1)
                      (item-score (at map ghostlocs x y))))))

(define (best-score width height map ghostlocs x y s depth v)
  (set! left  (score width height map ghostlocs (- x 1) y (+ s v) depth))
  (set! right (score width height map ghostlocs (+ x 1) y (+ s v) depth))
  (set! up    (score width height map ghostlocs x (- y 1) (+ s v) depth))
  (set! down  (score width height map ghostlocs x (+ y 1) (+ s v) depth))
  (set! minscore (min4 left right up down))
  (set! maxscore (max4 left right up down))
  (if (< 0 minscore) minscore maxscore))

(define (findpill map ghostlocs x y dir step width height dist)
  (if (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) (- 10000 dist)
    (do (set! val (at map ghostlocs x y))
      (if (or (= val 2) (or (= val 3) (= val 4))) dist
        (if (= val 1)
          (if (= dir 0)
            (findpill map ghostlocs (+ x step) y dir step width height (+ dist 1))
            (findpill map ghostlocs x (+ y step) dir step width height (+ dist 1))) 
          (- 10000 dist))))))

(define (penalty s d oppd)
  (if (= d oppd)
    (- s 30) s))

(define (mod x y)
  (- x (* (/ x y) y)))

(define (map list func)
  (if (atom? list) list
    (cons (func (car list)) (map (cdr list) func))))

(define (getloc x) (cons (car x ) (cadr x)))

(define (cmploc a b) (and (= (car a) (car b)) (= (cdr a) (cdr b))))

(define (item-val v)
  (cond ((= v 2) 1)
        ((= v 3) 5)
        ((= v 4) 10)
        ((= v 7) 4)
        (else 0)))

(define (dfs width height map ghostlocs fruit x y vislist depth md)
  (if (or (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) (>= depth md)) (+ 10000 depth)
    (do (set! val (at map ghostlocs fruit x y))
      (if (= val 0) 10000
        (if (= val 6) 100000
          (if (find1 vislist (cons x y) cmploc) (+ 10000 depth)
            (if (or (= val 2) (or (= val 3) (or (= val 4) (= val 7)))) (- depth (item-val val))
              (do
                (set! nv (cons (cons x y) vislist))
                (set! nd (+ depth 1))
                (set! scoreleft (dfs width height map ghostlocs fruit (- x 1) y nv nd md))
                (set! md (min scoreleft md))
                (set! scoreright (dfs width height map ghostlocs fruit (+ x 1) y nv nd md))
                (set! md (min scoreright md))
                (set! scoreup (dfs width height map ghostlocs fruit x (- y 1) nv nd md))
                (set! md (min scoreup md))
                (set! scoredown (dfs width height map ghostlocs fruit x (+ y 1) nv nd md))
                (set! md (min scoredown md)) md))))))))

(define (augmentlocs m)
  (if (atom? m) m
    (do
      (set! current (car m))
      (set! stat (car current))
      (set! x (cadr current))
      (set! y (cddr current))
      (cons current 
        (cons (cons stat (cons (- x 1) y))
              (cons (cons stat (cons (+ x 1) y))
                    (cons (cons stat (cons x (- y 1)))
                          (cons (cons stat (cons x (+ y 1))) (augmentlocs (cdr m))))))))))


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
  (set! ghostlocs (augmentlocs (augmentlocs (map ghoststate getloc))))
  ; (debug ghostlocs)
  (set! oppdir (mod (+ 2 dir) 4))
  (set! fruit (gettupleelem worldstate 3))
  ; (debug fruit)
  (set! depth 16)
  (set! sleft  (dfs width height worldmap ghostlocs fruit (- x 1) y 0 1 depth))
  (set! sright (dfs width height worldmap ghostlocs fruit (+ x 1) y 0 1 depth))
  (set! sup    (dfs width height worldmap ghostlocs fruit x (- y 1) 0 1 depth))
  (set! sdown  (dfs width height worldmap ghostlocs fruit x (+ y 1) 0 1 depth))
  ; (debug (cons sup (cons sright (cons sdown (cons sleft 0)))))
  (minidx (cons sup (cons sright (cons sdown (cons sleft 0))))))

(define (step aistate worldstate) 
  (set! move (make_move worldstate))
  (cons 0 move))

(define (main worldstate undocumented) 
  (cons 0 step))
