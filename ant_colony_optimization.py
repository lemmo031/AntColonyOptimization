;; Taken and modified from Uri Wilensky's 1997 Ant Colony Optimization NetLogo code.

globals [
  find-food-diffusion   ;; amount of diffusion for find-food-pheromone
  find-food-evaporation ;; amount of evaporation for find-food-pheromone
  find-hill-diffusion   ;; amount of diffusion for find-hill-pheromone
  find-hill-evaporation ;; amount of evaporation for find-hill-pheromone
]

patches-own [
  find-food-pheromone  ;; amount of find-food-pheromone on this patch
  find-hill-pheromone  ;; amount of find-hill-pheromone on this patch
  food                 ;; amount of food on this patch
  hill?                ;; true on hill patches, false elsewhere
  hill-scent           ;; number that is higher closer to the hill
  food-source-number   ;; number (1, 2, 3, or 4) to identify the food sources
]

;;;;;;;;;;;;;;;;;;;;;;;;
;;; Setup procedures ;;;
;;;;;;;;;;;;;;;;;;;;;;;;

to setup
  clear-all
  set-default-shape turtles "bug"
  create-turtles population
  [ set size 2
    set color red ]   ;; red = not carrying food and brown = carrying food
  setup-patches
  ;; Change the diffusion and evaporation rates for everything HERE:
  set find-food-diffusion 20
  set find-food-evaporation 8
  set find-hill-diffusion 1
  set find-hill-evaporation 8
  reset-ticks
end

to setup-patches
  ask patches
  [ setup-hill
    setup-food
    recolor-patch ]
end

to setup-hill ;; make 2 set ant hills
  if (distancexy (-0.9 * max-pxcor) (-0.8 * max-pycor)) < 3
  [ set hill? true ]

  if (distancexy (0.9 * max-pxcor) (0.8 * max-pycor)) < 3
  [ set hill? true ]

  ;; spread a hill-scent over the whole world -- stronger near the hill
  set hill-scent 200 - distancexy (-0.9 * max-pxcor) (-0.8 * max-pycor)
end

to setup-food ;; make 4 set food sources
  if (distancexy (0.6 * max-pxcor) (-0.1 * max-pycor)) < 3
  [ set food-source-number 1 ]

  if (distancexy (0.4 * max-pxcor) (-0.9 * max-pycor)) < 3
  [ set food-source-number 2 ]

  if (distancexy (0.2 * max-pxcor) (0.75 * max-pycor)) < 3
  [ set food-source-number 3 ]

  if (distancexy (-0.9 * max-pxcor) (0.7 * max-pycor)) < 3
  [ set food-source-number 4 ]

  if food-source-number > 0
  [ set food one-of [1 2 3 4 5] ]
end

to recolor-patch
  ;; give color to hill and food sources
  ifelse hill?
  [ set pcolor violet ] ;; all ant hills are violet
  [ ifelse food > 0 ;; each food source is a different color
    [ if food-source-number = 1 [ set pcolor cyan ]
      if food-source-number = 2 [ set pcolor sky  ]
      if food-source-number = 3 [ set pcolor blue ]
      if food-source-number = 4 [ set pcolor yellow ] ]
    ;; scale color to show find-food-pheromone concentration
    [ ifelse find-hill-pheromone > find-food-pheromone
      [ set pcolor scale-color green find-hill-pheromone 0.1 5 ]
      [ set pcolor scale-color orange find-food-pheromone 0.1 5 ] ] ]
end

;;;;;;;;;;;;;;;;;;;;;
;;; Go procedures ;;;
;;;;;;;;;;;;;;;;;;;;;

to go  ;; forever button
  ask turtles
    [ if who >= ticks [ stop ] ;; delay initial departure
      ifelse color = red
        [ look-for-food  ]       ;; not carrying food? look for it
        [ return-to-hill ]       ;; carrying food? take it back to hill
      wiggle
      fd 1 ]
  diffuse find-food-pheromone (find-food-diffusion / 100) ;; slowly diffuse find-food-pheromone
  diffuse find-hill-pheromone (find-hill-diffusion / 100) ;; slowly diffuse find-hill-pheromone
  ask patches
    [ set find-food-pheromone find-food-pheromone * (100 - find-food-evaporation) / 100  ;; slowly evaporate find-food-pheromone
      set find-hill-pheromone find-hill-pheromone * (100 - find-hill-evaporation) / 100  ;; slowly evaporate find-hill-pheromone
      recolor-patch ]
  tick
end

to return-to-hill
  ifelse hill?
    [ set color red ;; drop food and head out again
      rt 180 ]
    [ set find-food-pheromone find-food-pheromone + 60  ;; drop some find-food-pheromone
      uphill-hill-scent ]  ;; head toward the greatest value of hill-scent
end

to look-for-food
  ifelse food > 0
    [ set color brown + 1      ;; pick up food
      set food food - 1        ;; and reduce the food source
      rt 180                   ;; and turn around
      stop ]
    ;; go in the direction where the find-food-pheromone smell is strongest
    [ set find-hill-pheromone find-hill-pheromone + 60 ;; drop some find-hill-pheromone
      if (find-food-pheromone >= 0.05) and (find-food-pheromone < 2)  
        [ uphill-food-pheromone ] ]
end

;; sniff left and right, and go where the strongest smell is
to uphill-food-pheromone  ;; turtle procedure
  let scent-ahead food-pheromone-scent-at-angle   0
  let scent-right food-pheromone-scent-at-angle  45
  let scent-left  food-pheromone-scent-at-angle -45
  if (scent-right > scent-ahead) or (scent-left > scent-ahead)
    [ ifelse scent-right > scent-left
      [ rt 45 ]
      [ lt 45 ] ]
end

;; sniff left and right, and go where the strongest smell is
to uphill-hill-scent
  let scent-ahead hill-scent-at-angle   0
  let scent-right hill-scent-at-angle  45
  let scent-left  hill-scent-at-angle -45
  if (scent-right > scent-ahead) or (scent-left > scent-ahead)
    [ ifelse scent-right > scent-left
      [ rt 45 ]
      [ lt 45 ] ]
end

to wiggle
  rt random 40
  lt random 40
  if not can-move? 1 [ rt 180 ]
end

to-report hill-scent-at-angle [angle]
  let p patch-right-and-ahead angle 1
  if p = nobody [ report 0 ]
  report [hill-scent] of p
end

to-report food-pheromone-scent-at-angle [angle]
  let p patch-right-and-ahead angle 1
  if p = nobody [ report 0 ]
  report [find-food-pheromone] of p
end

to-report hill-pheromone-scent-at-angle [angle]
  let p patch-right-and-ahead angle 1
  if p = nobody [ report 0 ]
  report [find-hill-pheromone] of p
end
