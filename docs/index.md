

### GSoC22 Reports
<ul>
  {% for post in site.reports %}
      <li><a href="{{ post.url | remove_first:'/' }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>


### Contributers
<ul>
  {% for member in site.data.contributors %}
      <li>
        <a target="_blank" href="https://github.com/{{member.github}}">{{ member.name }} ({{ member.position }})</a>
      </li>
  {% endfor %}
</ul>
