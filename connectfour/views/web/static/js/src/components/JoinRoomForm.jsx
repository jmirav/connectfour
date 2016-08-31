import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import { emitAddUser } from '../emitters';


function mapStateToProps({ roomDoesNotExist }) {
  return {
    roomDoesNotExist,
  };
}


const propTypes = {
  roomDoesNotExist: PropTypes.bool.isRequired,
};


const JoinRoomForm = React.createClass({
  getInitialState: function() {
    return {
      username: ``,
      usernameError: null,
      room: ``,
      roomError: null,
    };
  },

  _handleInput: function(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  },

  _handleSubmit: function(e) {
    e.preventDefault();

    if (!this.state.room) {
      this.setState({
        roomError: 'Room required',
      });

      return;

    } else if (this.props.roomDoesNotExist) {
      this.setState({
        roomError: 'Room does not exist',
      });

      return;

    } else {
      this.setState({
        roomError: null,
      });
    }

    if (!this.state.username) {
      this.setState({
        usernameError: 'Username required',
      });

      return;

    } else {
      this.setState({
        usernameError: null,
      });
    }

    /*
    this.setState({
      usernameError: this.state.username ? null : 'Username required',
      roomError: this.state.room ? null : 'Room required',
    });

    if (this.state.usernameError || this.state.roomError) {
      return;
    }
    */

    emitAddUser({
      username: this.state.username,
      room: this.state.room,
    });

  },

  render: function() {
    let usernameError;

    if (this.state.usernameError) {
      usernameError = <span className="error">{this.state.usernameError}</span>;
    }

    let roomError;

    if (this.state.roomError) {
      roomError = <span className="error">{this.state.roomError}</span>;
    }

    return (
      <div>
        <h3>Join a game room?</h3>

        <form
          id="join-room-form"
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>
              <label htmlFor="room">
                Room ID
              </label>
            </dt>

            <dd>
              <input
                type="text"
                id="room"
                name="room"
                value={this.state.room}
                onChange={this._handleInput}
              />

              {roomError}
            </dd>

            <dt>
              <label htmlFor="username">
                Your username
              </label>
            </dt>

            <dd>
              <input
                type="text"
                id="username"
                name="username"
                value={this.state.username}
                onChange={this._handleInput}
              />

              {usernameError}
            </dd>
          </dl>

          <button type="submit">Submit</button>
        </form>
      </div>
    );
  },
});


JoinRoomForm.propTypes = propTypes;

export default connect(mapStateToProps)(JoinRoomForm);
