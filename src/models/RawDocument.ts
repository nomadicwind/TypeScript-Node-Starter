import mongoose from "mongoose";

export type RawDoc = mongoose.Document & {
    title: string;
    summary: string;
    rawContent: string;
    url: string;
    labels: string[];
    read: boolean;
    sourceType: string;
    imgUrl: string;
    notes: string;

}

const rawDocumentSchema = new mongoose.Schema<RawDoc> (
    {
        title: String,
        summary: String,
        rawContent: String,
        url: String,
        labels: Array,
        read: Boolean,
        sourceType: String,
        imgUrl: String,
        notes: String,
    },
    { timestamps: true },
);

export const RawDocument =  mongoose.model<RawDoc>("RawDocument", rawDocumentSchema);