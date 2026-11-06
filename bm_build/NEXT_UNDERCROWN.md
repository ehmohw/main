# Next: the Undercrown's placement (owner's report after 3.1h)

> "the undercrown's placement is really sloppy, resulting in major cut offs where the Netherrack is super flat and jarring
> looking. Furthermore, it would seem the underground generates with needless netherrack surrounding it, resulting in large
> blocky placements of it. Overall just very messy"

Plan (as the Underwater Kingdom's 3.1d settle - phase203/settle.py):
1. Find how phase237 places the Undercrown (template + its "filled over its box" biome/ground pass - phase203 notes it).
2. The flat cut-offs: the surface is levelled to one height across the whole footprint. Replace with a ring settle
   (settle.make with steep=/cap= as the kingdom's) that slopes the Nether's own terrain down/up to the structure's edge.
3. The blocky netherrack round the underground part: the template (or a fill) packs solid netherrack into the box around the
   underground rooms. Fill only real holes (settle 'under'/'fill' with sub=netherrack) instead of the whole box; let the
   natural cave terrain stay.
4. No falling blocks (gravel/soul sand: top-down clears, sub first - 3.1d's lessons), nothing past the Nether's ceiling.
5. Test: locate/force-build a few Undercrowns on the test server, sample edge height profiles (as kbuild.js did), count
   netherrack in the box vs before, screenshot if a renderer is available.
