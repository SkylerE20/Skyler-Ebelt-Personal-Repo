<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Burdell's Dogs</title>
</head>

<body>

    <div id="updateForm">
        <h2>Expense Form for: {{ $dogDetail->dog_name }}</h2>

        @if (session('success'))
            <div style="color: green;">
                {{ session('success') }}
            </div>
        @endif

        @if ($errors->any())
            <div style="color: red;">
                <ul>
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
	    @endif

        <form action="/expenseForm/{{ $dogDetail->dog_id }}" method="POST">
            @csrf

            <label for="newDate">Date:</label>
            <input type="date" id="newDate" name="newDate">
            
            <br/>
            <br/>

            <label for="newVendor">Vendor:</label>
            <input type="text" id="newVendor" name="newVendor">

            <br/>
            <br/>

            <label for="newCost">Cost:</label>
            <input type="number" id="newCost" name="newCost">

            <br/>
            <br/>

            <label for="select a category">Select a Category:</label>
            <select id="CategorySelector" name="newCategory">
                <option value="">Select a category</option>
                @foreach ($categories as $category)
                    <option value="{{ $category->category_name }}">{{ $category->category_name }}</option>
                @endforeach
            </select>
            
            <br/>
            <br/>
            <button type="submit">Add New Expense</button>
        </form>
    </div>

</body>
</html>
