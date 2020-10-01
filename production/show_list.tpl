<p>Todo List</p>
<table border="1">
 %for row in rows:
    <tr>
        <td>{{row[0]}}</td>
        <td>
             <a href="/update_item/{{row[0]}}">{{row[1]}}</a>
        </td>
        <td>
        %if row[2]==0:
            <a href="/set_status/{{row[0]}}/1">{{row[2]}}</a>
        %else:
            <a href="/set_status/{{row[0]}}/0">{{row[2]}}</a>
        %end
        <td>
            <a href="/delete_item/{{row[0]}}">Delete</a>
        <td>
    </tr>
%end
</table>

<a href="/new_item">New Item</a>
<!-- <a href="delete_item/14">We don't like 14</a> -->