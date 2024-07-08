//cd recipes\client
//npm start


// ---------------------------------------------------------------------IMPORTS-----------------------------------------------------------------------------
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// import { IoSearchCircle } from "react-icons/io5";
// import { FaTrash } from "react-icons/fa";
// import { FaEdit } from "react-icons/fa";
// import { FaPlusSquare } from "react-icons/fa";
// import { FaStar } from "react-icons/fa";


//serverless functions

function App() {


  // -------------------------------------------------------------------STATE VARIABLES-----------------------------------------------------------------
  // All recipes in the file
  const [fileContent, setFileContent] = useState([]);
  // A list of the newly created recipe info
  const [newRecipe, setNewRecipe] = useState({
    title: '',
    ingredients: '',
    instructions: '',
    tags: ''
  });
  // A list of the edited recipe info
  const [editedRecipe, setEditedRecipe] = useState({
    title: '',
    ingredients: '',
    instructions: '',
    tags: ''
  });
  // The index of the currently displayed recipe
  const [currentRecipe, setCurrentRecipe] = useState(0);
  // Whether or not to show the add recipe, edit recipe, or delete recipe forms
  const [showAddRecipe, setShowAddRecipe] = useState(false);
  const [showEditRecipe, setShowEditRecipe] = useState(false);
  const [showDeleteRecipe, setShowDeleteRecipe] = useState(false);
  // The name of the recipe the user entered to delete
  const [deleteRecipeName, setDeleteRecipeName] = useState('');



  // ----------------------------------------------------------FUNCTIONS TO FETCH FILE CONTENT------------------------------------------------------------------
  // Fetch file content on component mount
  useEffect(() => {
    fetchFileContent();
  }, []);

  const fetchFileContent = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/read-file');
      setFileContent(response.data.data);
      if (currentRecipe >= response.data.data.length) {
        setCurrentRecipe(response.data.data.length - 1);
      }
    } catch (error) {
      console.error('Error reading file:', error.response ? error.response.data : error.message);
    }
  };



  // ----------------------------------------------------------FUNCTIONS TO MAKE CHANGES THE FILE---------------------------------------------------------
  // Add the new recipe to the file
  const addRecipe = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/write-file', { 
      content_title: newRecipe.title,
      content_ingredients: newRecipe.ingredients,
      content_instructions: newRecipe.instructions,
      content_tags: newRecipe.tags });
      alert('Recipe added successfully');
      fetchFileContent();
      setNewRecipe({
        title: '',
        ingredients: '',
        instructions: '',
        tags: ''
      });
      showAddRecipeForm(false);
    } catch (error) {
      console.error('Error writing to file:', error.response ? error.response.data : error.message);
    }
  };



  // edit the selected recipe in the file
  const editRecipe = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/update-file', {
        index: currentRecipe,
        content_title: editedRecipe.title,
        content_ingredients: editedRecipe.ingredients,
        content_instructions: editedRecipe.instructions,
        content_tags: editedRecipe.tags
      });
      alert('Recipe edited successfully');
      fetchFileContent();
      setEditedRecipe({
        title: '',
        ingredients: '',
        instructions: '',
        tags: ''
      });
      showEditRecipeForm(false);
    } catch (error) {
      console.error('Error editing file:', error.response ? error.response.data : error.message);
    }
  };



  // delete seclected recipe from the file
  const deleteRecipe = async (e) => {
    e.preventDefault();
    setDeleteRecipeName('');
    if (fileContent[currentRecipe][0] === deleteRecipeName) {
      try {
        await axios.post('http://localhost:5000/api/delete-file', { content: currentRecipe });
        alert('Recipe deleted successfully');
        showDeleteRecipeForm(false);
        fetchFileContent();
      } catch (error) {
        console.error('Error deleting file:', error.response ? error.response.data : error.message);
      }
    } else {
      alert('Recipe name does not match.');
    }
  };



  // ---------------------------------------------FUNCTIONS TO DISPLAY AND RECEIVE RECIPE DATA TO AND FROM THE USER------------------------------------------
  
  // Switch the recipe being displayed
  const switchDisplayedRecipe = (index) => {
    setCurrentRecipe(index);
  };



  // FUNCTIONS SHOW AND ADD NEW RECIPE DATA
  // Show the add recipe form
  const showAddRecipeForm = (isVisible) => {
    setShowAddRecipe(isVisible);
    setShowEditRecipe(false);
    setShowDeleteRecipe(false);
  };

  // change the new recipe info to match the info the user entered
  const addNewRecipeData = (e) => {
    const { name, value } = e.target;
    setNewRecipe({ ...newRecipe, [name]: value });
  };



  // FUNCTIONS SHOW AND ADD EDITED RECIPE DATA
  // Show the edit recipe form
  const showEditRecipeForm = (isVisible) => {
    setShowEditRecipe(isVisible);
    setShowDeleteRecipe(false);
    setShowAddRecipe(false);
  };

  // change the edited recipe info to match the changes the user made
  const addEditedRecipeData = (e) => {
    const { name, value } = e.target;
    setEditedRecipe(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  // Show the edit recipe form and set the edited recipe info to the current recipe info
  const showFormAndCurrentInfo = (index) => {
    setCurrentRecipe(index);
    showEditRecipeForm(true);
    setEditedRecipe({
      title: fileContent[index][0],
      ingredients: fileContent[index][1],
      instructions: fileContent[index][2],
      tags: fileContent[index][3]
    });
  };
  


  // FUNCTIONS SHOW AND ADD DELETE RECIPE DATA
  // Show the delete recipe form
  const showDeleteRecipeForm = (isVisible) => {
    setShowDeleteRecipe(isVisible);
    setShowEditRecipe(false);
    setShowAddRecipe(false);
  };

  // gets the name of the recipe the user entered to delete
  const handleDeleteInputChange = (e) => {
    setDeleteRecipeName(e.target.value);
  };


  // ----------------------------------------------------------------RENDERING THE APP-------------------------------------------------------------
  return (
    <div className="App">

      <div className="cookbook">
        <h1>Recipes</h1>
        {fileContent.map((group, index) => (
          <button key={index} onClick={() => switchDisplayedRecipe(index)}>{group[0]}</button>
        ))}
      </div>

      <div className='cookbook_buttons'>
        <button onClick={() => showAddRecipeForm(true)}>Add Recipe</button>
        {fileContent && fileContent[currentRecipe] && fileContent[currentRecipe][0] && (
          <button onClick={() => showDeleteRecipeForm(true)}>Delete {fileContent[currentRecipe][0]}</button>
        )}
        {fileContent && fileContent[currentRecipe] && fileContent[currentRecipe][0] && (
          <button onClick={() => showFormAndCurrentInfo(currentRecipe)}>Edit {fileContent[currentRecipe][0]}</button>
        )}
      </div>

      <main>
        {fileContent.length > 0 && (
          <div className="recipe">
            <h1 className='recipe_title'>{fileContent[currentRecipe][0]}</h1>
            <ul>
              {fileContent[currentRecipe][1].split(', ').map((ingredient, i) => (
                <li key={i}>{ingredient.trim()}</li>
              ))}
            </ul>
            <ol>
              {fileContent[currentRecipe][2].split(' - ').map((instruction, i) => (
                <li key={i}>{instruction.trim()}</li>
              ))}
            </ol>
            <img src={fileContent[currentRecipe][3]} alt={`tags for ${fileContent[currentRecipe][0]}`} />
          </div>
        )}

        <form onSubmit={addRecipe} style={{ display: showAddRecipe ? 'block' : 'none' }}>
          <div className="new_recipe_form">
            <h3 className='form_title'>Create New Recipe</h3>
            <input type="text" name="title" className="title_input" placeholder="Enter Recipe Name" value={newRecipe.title} onChange={addNewRecipeData} required />
            <textarea type="text" name="ingredients" className="ingredients_input" placeholder="Enter Ingredients separated by commas. example: flour, sugar, salt" value={newRecipe.ingredients} onChange={addNewRecipeData} required />
            <textarea type="text" name="instructions" className="instructions_input" placeholder="Enter Instructions separated by dashes. example: step 1 - step 2 - step 3" value={newRecipe.instructions} onChange={addNewRecipeData} required />
            <input type="text" name="tags" className="tags_input" placeholder="Enter tags URL / file path. If no tags, type 'none'" value={newRecipe.tags} onChange={addNewRecipeData} required />
            <div className="button_group">
              <button type="submit">Add Recipe</button>
              <button type="button" onClick={() => showAddRecipeForm(false)}>Cancel</button>
            </div>
          </div>
        </form>

        <form onSubmit={editRecipe} style={{ display: showEditRecipe ? 'block' : 'none' }}>
          <div className="edit_recipe_form">
            {fileContent[currentRecipe] && (
              <>
                <h3 className='form_title'>Edit {fileContent[currentRecipe][0]}</h3>
                <input type="text" name="title" className="title_input" placeholder="Enter Recipe Name" value={editedRecipe.title} onChange={addEditedRecipeData} required />
                <textarea type="text" name="ingredients" className="ingredients_input" placeholder="Enter Ingredients separated by commas. example: flour, sugar, salt" value={editedRecipe.ingredients} onChange={addEditedRecipeData} required />
                <textarea type="text" name="instructions" className="instructions_input" placeholder="Enter Instructions separated by dashes. example: step 1 - step 2 - step 3" value={editedRecipe.instructions} onChange={addEditedRecipeData} required />
                <input type="text" name="tags" className="tags_input" placeholder="Enter tags URL / file path. If no tags, type 'none'" value={editedRecipe.tags} onChange={addEditedRecipeData} required />
              </>
            )}
            <div className="button_group">
              <button type="submit">Edit Recipe</button>
              <button type="button" onClick={() => showEditRecipeForm(false)}>Cancel</button>
            </div>
          </div>
        </form>


        <form onSubmit={deleteRecipe} style={{ display: showDeleteRecipe ? 'block' : 'none' }}>
          <div className="delete_recipe_form">
            <h3 className='form_title'>Are you sure you want to delete this recipe?</h3>
            <input type="text" name="name" className="name_input" placeholder="Enter Recipe Name to confirm. Your input will be case sensitive" value={deleteRecipeName} onChange={handleDeleteInputChange} required />
            <div className="button_group">
              <button type="submit">Yes</button>
              <button type="button" onClick={() => showDeleteRecipeForm(false)}>No</button>
            </div>
          </div>
        </form>


      </main>

    </div>
  );
}

export default App;
