const express = require("express");
const router = express.Router();
const fetchuser = require("../middleware/fetchuser");
const Note = require("../models/Note");
const { body, validationResult } = require("express-validator");

//  Fetch all notes using GET "notes/fetchallnotes" | Login Required
router.get("/fetchallnotes", fetchuser, async (req, res) => {
  const notes = await Note.find({ user: req.user.id });
  res.json(notes);
});

//  Add a new note using POST "notes/addnote" | Login Required
router.post(
  "/addnote",
  fetchuser,
  [
    body("title", "Title should be minimum of five characters.").isLength({
      min: 5,
    }),
    body(
      "description",
      "Description should be minimum of twenty characters."
    ).isLength({
      min: 20,
    }),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({status:false, errors: errors.array() });
      }

      const { title, description, tag } = req.body;

      const note = new Note({
        title,
        description,
        tag,
        user: req.user.id,
      });

      await note.save();

      res.status(200).json({status:true, message: "Note added successfully." });
    } catch (error) {
      console.log(error.message);
      return res.status(500).json({ status:false, message: "Internal Server Error" });
    }
  }
);

//  Update an existing note using PUT "notes/updatenote/:id" | Login Required
router.put(
  "/updatenote/:id",
  fetchuser,
  [
    body("title", "Title should be minimum of five characters.").isLength({
      min: 5,
    }),
    body(
      "description",
      "Description should be minimum of twenty characters."
    ).isLength({
      min: 20,
    }),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const newNote = {};
      const { title, description, tag } = req.body;
      if (title) {
        newNote.title = title;
      }
      if (description) {
        newNote.description = description;
      }
      if (tag) {
        newNote.tag = tag;
      }

      const note = await Note.findById(req.params.id);
      if (!note) {
        return res.status(404).json({ message: "Note not found." });
      }

      if (note.user.toString() !== req.user.id) {
        return res.status(401).json({ message: "Unauthorized user." });
      }

      await Note.findByIdAndUpdate(
        req.params.id,
        { $set: newNote },
        { new: true }
      );

      res.status(200).json({ message: "Note updated successfully." });
    } catch (error) {
      console.log(error.message);
      return res.status(500).json({ message: "Internal Server Error" });
    }
  }
);

//  Delete an existing note using DELETE "notes/deletenote/:id" | Login Required
router.delete("/deletenote/:id", fetchuser, [], async (req, res) => {
  try {
    const note = await Note.findById(req.params.id);
    if (!note) {
      return res.status(404).json({ message: "Note not found." });
    }

    if (note.user.toString() !== req.user.id) {
      return res.status(401).json({ message: "Unauthorized user." });
    }

    await Note.findByIdAndDelete(req.params.id);

    res.status(200).json({ message: "Note deleted successfully." });
  } catch (error) {
    console.log(error.message);
    return res.status(500).json({ message: "Internal Server Error" });
  }
});

module.exports = router;
