# Learning guide

Make small edits and preview after each one. Use Git history before experiments so you can inspect or undo a change.

## Checkpoint 1: Find your way around

Open index.html and locate the hero, four service cards, animated WhatsApp examples, process, portfolio note, FAQ, and contact sections. Change one sentence. Checkpoint: the copy changes without breaking the heading structure or navigation links.

## Checkpoint 2: Tune the palette

In css/styles.css, change the green or gold variable near the top. Review the buttons, hero chat, four service sketches, workflow simulator, and contact dialog. Checkpoint: focus rings and text remain easy to see.

## Checkpoint 3: Learn what each service includes

Read each service-card heading and paragraph in index.html, then find its matching service illustration in css/styles.css. Change one descriptive line or a small visual label. Checkpoint: the nearby text stays clear if animations are disabled, and the animation does not suggest a client result.

## Checkpoint 4: Adjust a gentle animation

Find a service keyframes rule near the service-card styles. Change a duration or small movement amount. Checkpoint: the motion remains restrained, and the reduced-motion rule still stops it. Do not use rapid flashing.

## Checkpoint 5: Edit a sample conversation

Open js/workflow-demo.js and find the workflows object. Change a fictional chatbot greeting or one of its quick-reply choices. Checkpoint: select that business tab, play the example, then pause and restart it. Keep every business clearly labeled as an example and do not add client results.

## Checkpoint 6: Add a real project

Update the portfolio note only with a real, approved project. Include the context, the team's exact role, what was built, approved media, and a verified outcome. Do not invent a client, metric, testimonial, or certification. Checkpoint: a new visitor can tell what is factual and what is illustrative. Use [CASE_STUDY_WORKSHEET.md](CASE_STUDY_WORKSHEET.md) to collect details and written permission first.

## Checkpoint 7: Try contact actions

Click the email and each phone number. Checkpoint: the email dialog offers Gmail and copy; each phone dialog offers the phone app and copy. Test keyboard focus and Escape. The phone links use the supplied digits without an assumed country code.

To show a WhatsApp button, confirm which business line is WhatsApp, then add its complete international digits to whatsappNumber and set its confirmation flag to true in js/config.js. Do not guess which supplied number is the WhatsApp line.

## Checkpoint 8: Review access and motion

Use Tab, Enter, and the arrow keys in the workflow tabs. Turn on reduced motion and replay a workflow. Checkpoint: all conversation and service descriptions remain readable without motion, and every control has a visible focus state.

## Checkpoint 9: Understand the login boundary

Read [SECURITY_AUTH.md](SECURITY_AUTH.md). The login integration is inactive until Supabase is configured. Checkpoint: explain why a hidden static page is not private and why passwords must never be stored in the repository.

## Checkpoint 10: Publish thoughtfully

Follow [DEPLOYMENT.md](DEPLOYMENT.md) and [SEO_GUIDE.md](SEO_GUIDE.md). Review the diff and deployment status. Checkpoint: the canonical URL and sitemap match the active HTTPS domain.
