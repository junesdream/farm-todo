import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./TodoList.css";
import { BiSolidTrash } from "react-icons/bi";

function TodoList({ listId, handleBackButton }) {
	const labelRef = useRef(null);
	const [listData, setListData] = useState(null);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const { data } = await axios.get(`/api/lists/${listId}`);
				setListData(data);
			} catch (error) {
				console.error("Failed to fetch list data:", error);
			}
		};
		fetchData();
	}, [listId]);

	async function handleCreateItem() {
		if (labelRef.current && labelRef.current.value) {
			try {
				const { data } = await axios.post(
					`/api/lists/${listData.id}/items/`,
					{ label: labelRef.current.value }
				);
				setListData(data);
				labelRef.current.value = "";
			} catch (error) {
				console.error("Failed to create item:", error);
			}
		}
	}

	async function handleDeleteItem(itemId) {
		try {
			const { data } = await axios.delete(
				`/api/lists/${listData.id}/items/${itemId}`
			);
			setListData(data);
		} catch (error) {
			console.error("Failed to delete item:", error);
		}
	}

	async function handleCheckToggle(itemId) {
		try {
			const { data } = await axios.patch(
				`/api/lists/${listData.id}/checked_state`,
				{
					item_id: itemId,
					checked_state: !listData.items.find(
						(item) => item.id === itemId
					).checked,
				}
			);
			setListData(data);
		} catch (error) {
			console.error("Failed to toggle check state:", error);
		}
	}

	if (!listData) {
		return (
			<div className="TodoList loading">
				<button className="back" onClick={handleBackButton}>
					Back
				</button>
				Loading to-do list...
			</div>
		);
	}

	return (
		<div className="TodoList">
			<button className="back" onClick={handleBackButton}>
				Back
			</button>
			<h1>List: {listData.name}</h1>
			<div className="box">
				<input ref={labelRef} placeholder="Add new item" type="text" />
				<button onClick={handleCreateItem}>Add Item</button>
			</div>
			{listData.items && listData.items.length > 0 ? (
				listData.items.map((item) => (
					<div
						key={item.id}
						className={`item ${item.checked ? "checked" : ""}`}
						onClick={() => handleCheckToggle(item.id)}
					>
						<span>{item.checked ? "✅" : "⬜️"} </span>
						<span className="label">{item.label}</span>
						<span
							className="trash"
							onClick={(e) => {
								e.stopPropagation();
								handleDeleteItem(item.id);
							}}
						>
							<BiSolidTrash />
						</span>
					</div>
				))
			) : (
				<div>There are currently no items.</div>
			)}
		</div>
	);
}

export default TodoList;
