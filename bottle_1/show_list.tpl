<p>Todo List</p>
<table border="1">
 %for row in rows:
    <tr>
    %for item in row:
        <td>{{item}}</td>
    %end
    </tr>
%end
</table>

<a href="/new_item">New Item</a>
