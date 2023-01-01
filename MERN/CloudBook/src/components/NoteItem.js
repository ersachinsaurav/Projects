import React, { useContext } from "react";
import noteContext from "../context/notes/noteContext";

function NoteItem(props) {
  const { note, editNoteModal } = props;
  const { deleteNote } = useContext(noteContext);

  return (
    <>
      <div className="col-md-3 my-3">
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{note.title}</h5>
            <p className="card-text">{note.description}</p>
            <i
              className="fa-solid fa-pen-to-square mx-"
              onClick={() => {
                editNoteModal(note);
              }}
            ></i>
            <i
              className="fa-solid fa-trash mx-2"
              onClick={() => {
                deleteNote(note._id);
                props.handleAlert("Note Deleted Successfully.", "success");
              }}
            ></i>
          </div>
        </div>
      </div>
    </>
  );
}

export default NoteItem;
