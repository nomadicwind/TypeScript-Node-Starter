import { NextFunction, Request, Response } from "express";
import { body, check, validationResult } from "express-validator";
import { RawDocument, RawDoc} from "../models/RawDocument";
import async from "async";
import { CallbackError, NativeError } from "mongoose";
import flash from "express-flash";

/**
 * Document management page.
 * @route GET /
 */
export const getDoc = (req: Request, res: Response) => {
    res.render("doc", {
        items: {},
    });
};

/**
 * Create a new doc manully
 * @route POST /doc
 */
export const postDoc = async (req: Request, res: Response, next: NextFunction) => {
    await check("title", "Title cannot be blank").not().isEmpty().run(req);
    await check("summary", "Summary is not valid").not().isEmpty().run(req);
    await check("rawContent", "Raw Content cannot be blank").not().isEmpty().run(req);


    const errors = validationResult(req);

    if (!errors.isEmpty()) {
        req.flash("errors", errors.array());
        return res.redirect("/doc");
    }

    const document = new RawDocument({
        title: req.body.title,
        summary: req.body.summary,
        rawContent: req.body.rawContent,
        url: req.body.url,
        labels: req.body.labels,
        read: req.body.read,
        imgUrl: req.body.imgUrl,
        notes: req.body.notes,
        sourceType: req.body.sourceType,
    });

    RawDocument.findOne({title: req.body.title}, (err: NativeError, existingDoc: RawDoc) => {
        if (err) { return next(err); }
        if (existingDoc) {
            req.flash("errors", { msg: "Document already exists." });
            return res.redirect("/doc");
        }
        document.save((err) => {
            if (err) { return next(err); }
        });
        res.status(201).send({ message: "Document created successfully" });
    });
};

const naviMenu = [
  {
    title: "All"
  },
  {
    title: "by Source",
    children: [
      {title: "Hacker News"},
      {title: "Feedly"},
    ]
  },
  {
    title:"by Type",
    children:[
      {title: "Tech"},
      {title: "Biz"},
    ]
  },
  {
    title: "Bookmarked"
  },
];


/**
 * List recent docs by default order 
 * @route /doc/list
 */
export const listDocs = async(req: Request, res: Response) => {
    try {
        const items = await RawDocument.find().sort({createdAt : -1});
        
        console.log("aaa " + items);
        res.render("doc",{items: items, navi: naviMenu});
      } catch (err) {
        req.flash("errors", { msg: err });
      }
};


export const markAsRead = async(req: Request, res: Response) => {
    try {

        // Assuming the field to update is `read` and the new value is in req.body.read
        const updatedDoc = await RawDocument.findByIdAndUpdate(
          req.params.id,
          { $set: { read: req.body.read } },
          { new: true }
        );
    
        if (!updatedDoc) {
          res.status(404).json({ message: "Document not found" });
        } else {
          res.json(updatedDoc);
          res.status(200).send({ message: "Document updated successfully" });
        }
      } catch (err) {
        res.status(500).json({ message: err.message });
      }
};