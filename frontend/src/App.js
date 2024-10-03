import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import ListToDoLists from "./ListTodoLists/ListTodoLists";
import TodoList from "./TodoList/TodoList";

function App() {
	const [listSummaries, setListSummaries] = useState(null);
	const [selectedItem, setSelectedItem] = useState(null);

	useEffect(() => {
		reloadData().catch(console.error);
	}, []);

	// Lade alle To-Do-Listen vom Backend
	async function reloadData() {
		try {
			const response = await axios.get("/api/lists");
			console.log("Fetched Data: ", response.data);
			setListSummaries(response.data);
		} catch (error) {
			console.error("Error loading lists", error); // Log detailed error
		}
	}

	// Funktion zum Erstellen einer neuen To-Do-Liste
	function handleNewToDoList(newName) {
		const updateData = async () => {
			const newListData = { name: newName };
			await axios.post(`/api/lists`, newListData);
			reloadData();
		};
		updateData();
	}

	// Funktion zum Löschen einer To-Do-Liste
	function handleDeleteToDoList(id) {
		const updateData = async () => {
			await axios.delete(`/api/lists/${id}`);
			reloadData();
		};
		updateData();
	}

	// Funktion zur Auswahl einer Liste
	function handleSelectList(id) {
		setSelectedItem(id);
	}

	// Funktion, um zurück zur Liste zu wechseln
	function backToList() {
		setSelectedItem(null);
		reloadData();
	}

	// Wenn keine Liste ausgewählt ist, zeige alle Listen
	if (selectedItem === null) {
		return (
			<div className="App">
				<ListToDoLists
					listSummaries={listSummaries}
					handleSelectList={handleSelectList}
					handleNewToDoList={handleNewToDoList}
					handleDeleteToDoList={handleDeleteToDoList}
				/>
			</div>
		);
	} else {
		return (
			<div className="App">
				<TodoList listId={selectedItem} handleBackButton={backToList} />
			</div>
		);
	}
}

export default App;
