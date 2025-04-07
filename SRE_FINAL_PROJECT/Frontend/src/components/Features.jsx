import React from 'react';

const Features = () => {
  const services = [
    { title: 'Civil Law', description: 'Expert legal advice on civil disputes.' },
    { title: 'Criminal Law', description: 'Top-notch criminal defense services.' },
    { title: 'Family Law', description: 'Assisting families through legal matters.' },
    { title: 'Patent Law', description: 'Protect your intellectual property.' },
  ];

  return (
    <div className="container my-5">
      <h2 className="text-center mb-4">Our Services</h2>
      <div className="row">
        {services.map((service, index) => (
          <div className="col-md-3 mb-4" key={index}>
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{service.title}</h5>
                <p className="card-text">{service.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Features;
