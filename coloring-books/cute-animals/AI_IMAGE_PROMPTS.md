# Cute Animals Coloring Book — 42 AI Image Prompts

Use these in **Midjourney, DALL·E 3, Leonardo, Ideogram, or any AI image tool**
to generate the exact polished, cute, hand-illustrated coloring style shown in
the reference. Generate **one page at a time**, then use `assemble_from_images.py`
to compile them into the print-ready 8.5 × 11 in PDF.

---

## STYLE BLOCK (already included in each prompt below)
> black and white coloring book line art, bold clean smooth outlines, cute
> kawaii style, big sparkly expressive eyes, rounded friendly features, large
> open white areas to color, pure white background, no shading, no grey, no
> color, no text, centered composition with comfortable margins, professional
> children's coloring book illustration, 8.5x11 portrait, 300 DPI.

### Midjourney tip
Append ` --ar 17:22 --style raw --no color,shading,grey,text` to each prompt.
(17:22 ≈ 8.5×11.) For DALL·E/Leonardo just paste the prompt as-is.

### Consistency rule
Keep line thickness, eye design, and cuteness identical across all 42 so the
book looks like one artist drew it.

---

## COVER PROMPT
Cute animals coloring book COVER, full color, a happy group of adorable baby
animals together in a sunny flower meadow — fluffy puppy, kitten with a bow,
bunny, baby deer, duckling, raccoon, hedgehog — big sparkly eyes, soft cartoon
style, blue sky, green trees, colorful flowers, cheerful and heartwarming,
professional children's book cover, vibrant, 8.5x11 portrait. (Add your title
text in Canva afterward.)

---

## THE 42 PAGES
Each line = paste directly. All begin with the SUBJECT, then the STYLE BLOCK.

1. Cute fluffy puppy sitting in a flower garden, wagging tail, big sparkly eyes — [STYLE BLOCK]
2. Adorable kitten playing with fluttering butterflies among flowers — [STYLE BLOCK]
3. Happy bunny surrounded by spring flowers, long floppy ears — [STYLE BLOCK]
4. Baby elephant holding a single flower with its trunk, tiny ears — [STYLE BLOCK]
5. Cute panda sitting and eating bamboo, round belly — [STYLE BLOCK]
6. Baby deer with tiny spots resting among wildflowers — [STYLE BLOCK]
7. Little hedgehog carrying a bundle of flowers on its back — [STYLE BLOCK]
8. Friendly owl perched on a tree branch under a crescent moon and stars — [STYLE BLOCK]
9. Cute fox curled up sleeping beneath a crescent moon and stars — [STYLE BLOCK]
10. Happy turtle swimming with little tropical fish and bubbles — [STYLE BLOCK]
11. Baby llama standing in a mountain meadow with a decorated saddle blanket — [STYLE BLOCK]
12. Cute koala hugging a eucalyptus tree branch — [STYLE BLOCK]
13. Baby lion with a fluffy mane sitting among savanna flowers — [STYLE BLOCK]
14. Happy monkey holding a banana, sitting on a vine — [STYLE BLOCK]
15. Cute giraffe with a long neck surrounded by butterflies — [STYLE BLOCK]
16. Baby zebra with stripes standing in a grassy field — [STYLE BLOCK]
17. Adorable hippo playing beside a pond with lily pads — [STYLE BLOCK]
18. Happy crocodile wearing a flower crown, sitting in shallow water — [STYLE BLOCK]
19. Cute penguin holding a large snowflake, standing on ice — [STYLE BLOCK]
20. Baby polar bear playing in soft snow with snowflakes falling — [STYLE BLOCK]
21. Friendly dolphin jumping above ocean waves — [STYLE BLOCK]
22. Cute whale swimming with small fish and rising bubbles — [STYLE BLOCK]
23. Baby seal resting on the beach beside seashells and a starfish — [STYLE BLOCK]
24. Happy octopus surrounded by bubbles and a starfish — [STYLE BLOCK]
25. Cute seahorse swimming gracefully through coral — [STYLE BLOCK]
26. Baby duck splashing playfully in a small pond — [STYLE BLOCK]
27. Cute fluffy chick standing among spring flowers — [STYLE BLOCK]
28. Happy lamb with curly wool resting in a peaceful meadow — [STYLE BLOCK]
29. Baby goat with tiny horns standing beside a country fence — [STYLE BLOCK]
30. Cute piglet playing among daisies, curly tail — [STYLE BLOCK]
31. Happy calf with spots standing in a flower-filled farm field — [STYLE BLOCK]
32. Cute horse with a flowing mane surrounded by countryside flowers — [STYLE BLOCK]
33. Baby raccoon holding a small flower in its paws — [STYLE BLOCK]
34. Cute squirrel collecting acorns, big bushy tail — [STYLE BLOCK]
35. Happy bear cub having a woodland picnic with a basket — [STYLE BLOCK]
36. Cute sloth hanging gently from a tree branch, sleepy smile — [STYLE BLOCK]
37. Baby kangaroo with a joey peeking from its pouch — [STYLE BLOCK]
38. Cute alpaca with fluffy wool surrounded by cactus flowers — [STYLE BLOCK]
39. Happy frog sitting on a lily pad in a pond — [STYLE BLOCK]
40. Cute snail with a spiral shell exploring a mushroom garden — [STYLE BLOCK]
41. Adorable puppy, kitten and bunny sitting together as best friends — [STYLE BLOCK]
42. Grand finale: several cute baby animal friends celebrating together in a flower meadow with bunting flags and sunshine — [STYLE BLOCK]

---

### Workflow to finish the book
1. Generate each page above (aim for clean line art; regenerate any with stray grey/shading).
2. Save them as `img/page_01.png` … `img/page_42.png` (white background, high resolution).
3. Optionally save a `img/cover.png`.
4. Run `python3 assemble_from_images.py` → produces `Cute-Animals-FINAL.pdf` (8.5×11, 300 DPI, KDP-ready).
