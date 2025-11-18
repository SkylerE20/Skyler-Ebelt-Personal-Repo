<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Burdell's Dogs</title>
</head>
<body>
    <div>
        <h2>Login</h2>
        <form action="/login" method="POST">
            @csrf
            <input name="lemail" type="text" placeholder="Email">
            <input name="lpassword" type="password" placeholder="Password">
            <button>Login</button>
        </form>
    </div>

    @if ($errors->has('lemail'))
        <div style="color: red;">
            {{ $errors->first('lemail') }}
        </div>
    @endif

    @if ($errors->has('lpassword'))
        <div style="color: red;">
            {{ $errors->first('lpassword') }}
        </div>
    @endif
    
</body>
</html>