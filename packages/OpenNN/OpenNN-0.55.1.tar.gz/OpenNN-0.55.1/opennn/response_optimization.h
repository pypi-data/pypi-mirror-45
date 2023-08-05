/****************************************************************************************************************/
/*                                                                                                              */
/*   OpenNN: Open Neural Networks Library                                                                       */
/*   www.opennn.net                                                                                             */
/*                                                                                                              */
/*   R E S P O N S E   O P T I M I Z A T I O N   C L A S S   H E A D E R                                        */
/*                                                                                                              */
/*   Artificial Intelligence Techniques SL                                                                      */
/*   artelnics@artelnics.com                                                                                    */
/*                                                                                                              */
/****************************************************************************************************************/

#ifndef __RESPONSEOPTIMIZATION_H__
#define __RESPONSEOPTIMIZATION_H__

// System includes

#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>

// OpenNN includes

#include "vector.h"
#include "matrix.h"
#include "neural_network.h"

// TinyXml includes

#include "tinyxml2.h"

namespace OpenNN
{

class ResponseOptimization
{

public:

   // DEFAULT CONSTRUCTOR

    explicit ResponseOptimization();

    explicit ResponseOptimization(NeuralNetwork*);

   // DESTRUCTOR

   virtual ~ResponseOptimization();

   enum Condition{Between, EqualTo, LessEqualTo, GreaterEqualTo, Minimum, Maximum};

   struct Results
   {
       /// Default constructor.

       explicit Results(){}

       virtual ~Results(){}

       Vector<double> optimal_inputs;
       Vector<double> optimal_targets;

       double objective_value;
   };


   void set_input_condition(const string&, const Condition&, const Vector<double>& = Vector<double>());
   void set_output_condition(const string&, const Condition&, const Vector<double>& = Vector<double>());

   void set_input_condition(const size_t&, const Condition&, const Vector<double>& = Vector<double>());
   void set_output_condition(const size_t&, const Condition&, const Vector<double>& = Vector<double>());

   Matrix<double> calculate_inputs() const;

   Matrix<double> calculate_envelope() const;

   Results* perform_optimization() const;

private:

    NeuralNetwork* neural_network_pointer;

    Vector<Condition> inputs_conditions;
    Vector<Condition> outputs_conditions;

    Vector<double> inputs_minimums;
    Vector<double> inputs_maximums;

    Vector<double> outputs_minimums;
    Vector<double> outputs_maximums;

    size_t samples_number = 10000;

    double calculate_random_uniform(const double&, const double&) const;

};

}

#endif


// OpenNN: Open Neural Networks Library.
// Copyright(C) 2005-2018 Artificial Intelligence Techniques, SL.
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software

// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

