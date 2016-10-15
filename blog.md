---
layout: singlePage
title: "Blog Posts"
---

# Blog Posts

<table class="table table-hover">
  {% for post in site.posts %}
    {% unless post.draft %}
    <tr>
     
    </tr>
    {% endunless %}
  {% endfor %}
</table>
