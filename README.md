<div class="container">

    <div class="row">
        <div class="col-lg-12 text-center">
            <h1></h1>

            <p class="lead">The web services are available as a SOAP service or REST services</p>
        </div>
    </div>
    <div class="row text-center">
        <div class="col-lg-6">
            <h1>SOAP</h1>
            username is root, password is F0T349M3RTo2
            <a href="{% url "soap" %}"><h3>http://localhost:8000/opensooq</h3></a>
        </div>
        <div class="col-lg-6">
            <h1>REST</h1>
            <ul>
                <li>
                    <strong>Add post</strong>(title, description, type)<strong>login required</strong><br>
                    example: http://localhost:8000/add/test_title/test_desc/test_type
                </li>
                <li class="margin-top">
                    <strong>Remove post</strong>(post_id)<strong>login required</strong><br>
                    example: http://localhost:8000/delete/0
                </li>
                <li class="margin-top">
                    <strong>update post</strong>(post_id, title, description, type)<strong>login required</strong><br>
                    example: http://localhost:8000/update/0/test_title/test_desc/test_type
                </li>
                <li class="margin-top">
                    <strong>search</strong>(term)<strong>login not required</strong><br>
                    example: http://localhost:8000/search/asd
                </li>
                <li class="margin-top">
                    <strong>list</strong>()<strong>login not required</strong><br>
                    example: http://localhost:8000/list
                </li>
            </ul>
        </div>
    </div>
    <!-- /.row -->

</div>
