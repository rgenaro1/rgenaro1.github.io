---
layout: index
title: Genaro Rodriguez
---


Soy ingeniero industrial graduado en la Universidad Nacional de Trujillo, tengo experiencia y capacitación en gestión de proyectos y en manufactura. 


{% include cv.md %}

## <i class="fa fa-chevron-right"></i> Post recientes

<table class="table table-hover">
  {% for post in site.posts limit: 5 %}
    {% unless post.draft %}
    <tr>
      
    </tr>
    {% endunless %}
  {% endfor %}
</table>
<h4><a href="/blog">View all</a></h4>

---

Last updated on {% include last-updated.txt %}
