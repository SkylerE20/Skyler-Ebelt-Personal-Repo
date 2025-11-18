/*
        $expenseList = DB::select("SELECT dog.dog_id AS dog_id,
        dog.dog_name as dog_name,
        expense.expense_date AS date, 
        expense.expense_vendor AS vendor,
	    expense.cost AS cost,
	    expense.category_name AS categoryname
        FROM expense AS expense
        INNER JOIN dog AS dog
        ON expense.dog_id = dog.dog_id; ");

        $dogs = DB::select("SELECT dog_id, dog_name FROM dog;");
*/

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Expense Form</title>
<script>
    function toggleUpdateForm() {
        const updateForm = document.getElementById('updateForm');
        updateForm.style.display = updateForm.style.display === 'none' ? 'block' : 'none';
    }
</script>
<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
</head>
<body>
    <h2>Expense Form</h2>
    <table>
        <tr>
            <th>Dog ID</th>
            <th>Dog Name</th>
            <th>Date</th>
            <th>Vendor</th>
            <th>Cost</th>
            <th>Category Name</th>
        </tr>

        @foreach($expenseList as $expense)
        <tr>
            <td>{{$expense->dog_id}}</td>
            <td>{{$expense->dog_name}}</td>
            <td>{{$expense->date}}</td>
            <td>{{$expense->vendor}}</td>
            <td>{{$expense->cost}}</td>
            <td>{{$expense->categoryname}}</td>
        </tr>
        @endforeach
    </table>
</body>

<br/>
<br/>

<button onclick="toggleUpdateForm()">Add New Expense</button>

<br/>
<br/>

<div id="updateForm" style="display:none;">
<form action="/addNewExpense" method="POST">
        @csrf

        <label for="select a dog">Select a dog:</label>
          <select id="dogSelector" name="newDogId">
            <option value="">Select a Dog</option>
             @foreach ($dogs as $dogTemp)
            <option value="{{ $dogTemp->dog_id }}">{{ $dogTemp->dog_name }}</option>
             @endforeach
          </select>

                <br/>
                <br/>

                <label for="Date">Date:</label>
                <input type="date" id="newDate" name="newDate">
                
                <br/>
                <br/>

                <label for="vendor">Vendor:</label>
                <input type="text" id="newVendor" name="newVendor">

                <br/>
                <br/>

                <label for="cost">Cost:</label>
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
</html>
