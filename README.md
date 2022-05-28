# lux-ai-agents-kenny-version

# main idea
- city tile:
    - if research point >= 200, then build worker and cart and make them balanced
    - if research point < 200, build worker and cart and make them balanced until we have 10 workers, and then do research
- worker:
    - if near night, then go home(city tile)
    - if cargo is full, then build city tile
    - if can collect resources, collect until cargo is full
    - if no condition above is satisfied, move toward the nearest cell which has resources
    
- cart:
    - if near night, or cargo is full, go home
    - move around workers

# problems

- make actions without considering the opponent's action
- doesn't use any knowledge about road
- ...