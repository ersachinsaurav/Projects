import React, { useContext, useEffect, useRef, useState } from "react";
import noteContext from "../context/notes/noteContext";
import NoteItem from "./NoteItem";
import AddNote from "./AddNote";
import { useNavigate } from "react-router-dom";

function Notes(props) {
  const { notes, getNotes, editNote } = useContext(noteContext);
  const ref = useRef(null);
  const refClose = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if(localStorage.getItem("authToken")){
      getNotes();
    }else{
      navigate("/login");
      props.handleAlert("Unauthorized Access.", "danger");
    }
    // eslint-disable-next-line
  }, []);

  const handleEditNoteModal = (currentNote) => {
    ref.current.click();
    setNote({
      id: currentNote._id,
      eTitle: currentNote.title,
      eDescription: currentNote.description,
      eTag: currentNote.tag,
    });
  };

  const [note, setNote] = useState({
    eTitle: "",
    eDescription: "",
    eTag: "",
  });

  const handleEditNote = () => {
    editNote(note.id, note.eTitle, note.eDescription, note.eTag);
    refClose.current.click();
    props.handleAlert("Note Updated Successfully.", "success");
  };

  const onChange = (e) => {
    setNote({ ...note, [e.target.name]: e.target.value });
  };

  return (
    <>
      <button
        type="button"
        className="btn btn-primary d-none"
        data-bs-toggle="modal"
        data-bs-target="#staticBackdrop"
        ref={ref}
      >
        Launch
      </button>

      <div
        className="modal fade"
        id="staticBackdrop"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabIndex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h1 className="modal-title fs-5" id="staticBackdropLabel">
                Edit Note
              </h1>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">
              <div className="my-3" id="editNote">
                <div className="mb-3">
                  <label htmlFor="eTitle" className="form-label">
                    Title
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="eTitle"
                    name="eTitle"
                    placeholder="Title of Note"
                    onChange={onChange}
                    value={note.eTitle}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="eDescription" className="form-label">
                    Description
                  </label>
                  <textarea
                    className="form-control"
                    id="eDescription"
                    name="eDescription"
                    placeholder="Description of Note"
                    rows="3"
                    onChange={onChange}
                    value={note.eDescription}
                  ></textarea>
                </div>
                <div className="mb-3">
                  <label htmlFor="eTag" className="form-label">
                    Tag
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="eTag"
                    name="eTag"
                    placeholder="Tag of Note"
                    onChange={onChange}
                    value={note.eTag}
                  />
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-bs-dismiss="modal"
                ref={refClose}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleEditNote}
                disabled={
                  note.eTitle.length < 5 || note.eDescription.length < 20
                }
              >
                Update Note
              </button>
            </div>
          </div>
        </div>
      </div>

      <AddNote handleAlert={props.handleAlert} />
      <div className="row my-3" id="yourNotes">
        <h2 className="mb-3">Your Notes</h2>
        {notes.length === 0 && (
          <div className="col-md-3 my-3">No Notes Found.</div>
        )}

        {notes.map((note) => {
          return (
            <NoteItem
              key={note._id}
              editNoteModal={handleEditNoteModal}
              note={note}
              handleAlert={props.handleAlert}
            />
          );
        })}
      </div>
    </>
  );
}

export default Notes;
