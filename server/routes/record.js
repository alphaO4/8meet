const express = require('express');
const path = require('path');

const recordRoutes = express.Router();
const dbo = require('../db/conn');

recordRoutes.route('/videos').get(async function (_req, res) {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection('videos')
    .find({})
    .limit(50)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send('Error fetching videos!');
      } else {
        res.json(result);
      }
    });
});

recordRoutes.route('/video/:title').get(function (req, res) {
  const dbConnect = dbo.getDb();
  const videoQuery = { title: req.params.title };

  const db_videos = dbConnect.collection("videos");
  const cursor = db_videos.find(videoQuery)

  cursor.count().then((video_count) => {
    if (video_count > 0) {
      // Return video to client
      res.sendFile("./public/" + req.params.title, { root: path.join(__dirname, "..") });
    } else {
      // Mach neues video
      const videoDocument = {
        title: req.params.title,
      };
      dbConnect
        .collection('videos')
        .insertOne(videoDocument, function (err, result) {
          if (err) {
            res.status(400).send('Error creating video!');
          } else {
            console.log(`Added a new video with id ${videoDocument._id}`);
            res.status(204).send();
          }
        });

    }
  }).catch((err) => {
    console.log(err);
  })
});

recordRoutes.route('/videos/delete/:_id').delete((req, res) => {
  const dbConnect = dbo.getDb();
  const videoQuery = { _id: req.body._id };

  dbConnect
    .collection('videos')
    .deleteOne(videoQuery, function (err, _result) {
      if (err) {
        res
          .status(400)
          .send(`Error deleting video with _id ${videoQuery._id}!`);
      } else {
        console.log('1 document deleted');
      }
    });
});

module.exports = recordRoutes;